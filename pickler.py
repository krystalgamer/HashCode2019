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

    min_threshold = 3
    if len(sys.argv) != 2:
        return

    show = pickle.load(open(sys.argv[1]+'.pickle', 'rb'))
    
    with open('sol'+sys.argv[1]) as f:
        f.write(str(len(show)) + '\n')
        for trans in show:
            if isinstance(trans.primeira, Slide):
                f.write(str(trans.primeira.photos.id)+'\n')
            f.write(str(trans.segunda.photos.id)+'\n')
    return

if __name__ == '__main__':
    main()
