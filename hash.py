import sys
import pickle

class Photo(object):
    def __init__(self, tipo, tags, ide):
        self.type = tipo
        self.tags = tags
        self.id = ide

    def is_vertical(self):
        return self.type == 'V'

    def common_tags(self, second):
        ret = []
        for tag in self.tags:
            if tag in second.tags:
                ret.append(tag)
        return ret


class Slide(object):

    def __init__(self, photos):
        self.photos = photos

    @property
    def tags(self):
        if isinstance(self.photos, Photo):
            return self.photos.tags
        return self.photos[0].tags + list(set(self.photos[1].tags) - set(self.photos[0].tags))

    def common_tags(self, second):
        ret = []
        for tag in self.tags:
            if tag in second.tags:
                ret.append(tag)
        return ret

    def interest_factor_slides(self, second):
        num_common_tags = len(self.common_tags(second))
        return min(len(self.tags)-num_common_tags, num_common_tags, len(second.tags)-num_common_tags)


class Transicao(object):

    def __init__(self, primeira, segunda):
        self.primeira = primeira
        self.segunda = segunda


def main():

    min_threshold = 15
    if len(sys.argv) != 2:
        return

    #print('Loading {}'.format(sys.argv[1]))

    texto = None
    with open(sys.argv[1]) as f:
        texto = f.readlines() 
    slides = []
    verticais = []
    cur_line = 0
    texto = texto[1:]
    for line in texto:
        line = line.split()
        tipo = line[0]
        num_tags = int(line[1])
        tags = line[2:2+num_tags]

        if tipo == 'H':
            slides.append(Slide(Photo(tipo, tags, cur_line)))
        else:
            verticais.append(Photo(tipo, tags, cur_line))
        cur_line+=1
    
    verticais.sort(key=lambda x: len(x.tags))
    if len(verticais) % 2 != 0:
        raise 'merda'

    for i in range(len(verticais)//2):
        slides.append(Slide([verticais[0], verticais[-1]]))
        verticais.pop(0)
        verticais.pop(-1)
    
    show = []
    last_slide = None
    got_it = False
    last_good = None
    last_good_interest = 0
    #Encontra primeira transicao
    for i in range(1, len(slides)):
        tmp = slides[0].interest_factor_slides(slides[i])
        if  tmp >= min_threshold:
            show.append(Transicao(slides[0], slides[i]))
            last_slide = slides[i]
            slides.pop(0)
            slides.pop(i-1)
            got_it = True
            break
        elif tmp>=1:
            if tmp > last_good_interest:
                last_good_interest = tmp
                last_good = i
            
    if got_it == False:
        show.append(Transicao(slides[0], slides[last_good]))
        last_slide = slides[i]
        slides.pop(0)
        slides.pop(last_good-1)
        
    #Encontra as outras transicoes
    iteracoes = int(len(slides)/2)
    last_interest = 0
    for i in range(iteracoes):

        found_least_best = False
        probable_slide = None
        for slide in slides:
            interest = last_slide.interest_factor_slides(slide)
            if interest >= min_threshold:
                #improvement
                last_slide = slide
                show.append(Transicao(None, last_slide))
                found_least_best = True
                break
            elif interest >= 1:
                if interest > last_interest:
                    probable_slide = slide

        if found_least_best:
            slides.remove(last_slide)
            continue

        if probable_slide == None:
            break
        
        last_slide = probable_slide
        show.append(Transicao(None, last_slide))
        slides.remove(last_slide)


    pickle.dump(show, open(sys.argv[1]+'.pickle', 'wb'))
    
    with open('sol_'+sys.argv[1], 'w') as f:
        f.write(str(len(show)+1) + '\n')
        for trans in show:
            if isinstance(trans.primeira, Slide):
                if isinstance(trans.primeira.photos, Photo):
                    f.write(str(trans.primeira.photos.id)+'\n')
                else:
                    f.write(str(trans.primeira.photos[0].id)+' '+str(trans.primeira.photos[1].id)+'\n')

            if isinstance(trans.segunda.photos, Photo):
                f.write(str(trans.segunda.photos.id)+'\n')
            else:
                f.write(str(trans.segunda.photos[0].id)+' '+str(trans.segunda.photos[1].id)+'\n')
    return

if __name__ == '__main__':
    main()
