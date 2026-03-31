from functools import partial

from yhttp.core import statuses


conflict_json = partial(statuses.conflict, encoder='json')
