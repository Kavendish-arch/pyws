import doctest

class Page(object):

    def __init__(self, start, count, total):
        self.start = start
        self.count = count
        self.total = total


    def is_have_previous_page(self):
        return self.start != 0

    def is_have_next_page(self):

        return self.start + self.count < self.total


    def get_total_page(self):
        """
        >>> page = Page(2,50, 500)
        >>> page.get_total_page()
        10
        >>> page = Page(2,50, 460)
        >>> page.get_total_page()
        10
        :return:
        """
        pages = self.total / self.count
        if 0 == self.total % self.count:
            pages = self.total / self.count
            return pages
        else:
            pages = int(self.total / self.count) + 1
            return


def get_page(request ):

    page_index = request.args.get("page")
    count = request.args.get("count")

    try:
        page_i = int(page_index)
        count = int(count)
    except ValueError:
        page_i = 1
        count = 30
    except BaseException:
        page_i = 1
        count = 30

    page_info = {
        'min_page_index': 1,
        'max_page_index': 10,
        'page_id': page_i,
        'count': count,
    }

    return page_info



if __name__=="__main__":

    page = Page(0, 10, 500)
    # assert page.get_total_page() == 50
