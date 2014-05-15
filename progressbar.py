from __future__ import print_function
import uuid
from IPython.display import HTML, Javascript, display_html, display_javascript
import sys

class ProgressBar(object):
    """Abstract class to be subclassed"""
    def __init__(self, iterations=100, progress=0, **kwargs):
        self.iterations = iterations
        self.progress = progress
        self._initialize()

    def animate(self, added_progress=1):
        self.progress += added_progress
        if self.progress >= self.iterations:
            self._remove()
        else:
            self._update()

    def _update(self):
        """Updates the progress bar - overload this"""
        pass

    def _initialize(self):
        """Initializes the progress bar - overload this"""
        pass

    def _remove(self):
        """removes the progressbar from view -overload this"""
        pass

    def __repr__(self):
        """Print progress"""
        return '{progress}/{iterations}'.format(**self.__dict__)


class ProgressBarASCII(ProgressBar):
    """Loading bar class based on ASCII characters"""
    def __init__(self, width=50, **kwargs):

        self.width = width
        super(ProgressBarASCII, self).__init__(**kwargs)
    
    def _initialize(self):
        self._update()
    
    def _update(self):
        self._percent = int(round((float(self.progress) / self.iterations) * 100.0))
        all_full = self.width - 2
        num_hashes = int(round((self._percent / 100.0) * all_full))
        self.prog_bar = '[' + '*' * num_hashes + ' ' * (all_full - num_hashes) + ']'
        pct_place = (len(self.prog_bar) // 2) - len(str(self._percent))
        pct_string = '%d%%' % self._percent
        self.prog_bar = self.prog_bar[0:pct_place] + \
            (pct_string + self.prog_bar[pct_place + len(pct_string):])
        print('\r', self, end='')
        sys.stdout.flush()

    def _remove(self):
        print('\r', end='')
        sys.stdout.flush()

    def __str__(self):
        return str(self.prog_bar)
    
    def __repr__(self):
        return str(self)



class ProgressBarHTML(ProgressBar):
    """Loading bar class with HTML5 and Javascript support"""
    def __init__(self, **kwargs):
        super(ProgressBarHTML, self).__init__(**kwargs)
    
    def _initialize(self):
        self.bar_id = str(uuid.uuid4())
        self.HTML = HTML(
                         """
                             <progress
                             value="{progress}"
                             max="{iterations}"
                             id="{id}">
                             </progress>
                             """.format(progress = self.progress,
                                        id = self.bar_id,
                                        iterations = self.iterations))
        display_html(self.HTML)
        self._update()

    def _update(self):
        display_javascript(Javascript("$('progress#{id}').val('{progress}')"\
                    .format(id = self.bar_id, progress = self.progress)))
        
    def _remove(self):
        display_javascript(Javascript(
        """var elem = document.getElementById('{id}'); elem.parentNode.removeChild(elem);""".format(id = self.bar_id)))

    def __str__(self):
        return str(self.progress)



class ProgIter:
    """
    Iterator implementing a progress bar. Supply a size of your iterable with size
     if known to avoid having to iterate through anyway.
     """
    def __init__(self, iterable, progress_bar=None, size=None, rich=False):
        if size is None:
            self.size = len(iterable)
        else:
            self.size = size
        if progress_bar is None:
            if rich:
                self.pbar = ProgressBarHTML(iterations=100)
            else:
                self.pbar = ProgressBarASCII(iterations=100)
        else:
            self.pbar = progress_bar

        self.iterator = iter(iterable)
        self.curr = 0
        self.adv = self.size/100

    def __getitem__(self, index):
        self.curr += 1
        a = next(self.iterator)
        if self.curr % self.adv == 0:
            self.pbar.animate()
        return a

