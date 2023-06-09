from datetime import datetime

from src.utils import io


class Config:
    def __init__(self, filename=None):
        self._config = {}
        if filename is not None:
            dict_ = io.read_json(filename)
            for k, v in dict_.items():
                self[k] = v

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value
        setattr(self, key, value)

    def __iter__(self):
        return iter(self._config.items())

    def __repr__(self):
        out = 'Config('
        for k, v in self:
            out += f'\n* {k}: {v}'
        out += ')'
        return out

    def save(self, filename):
        io.to_json(self._config, filename)

    def update(self, dict_):
        for k, v in dict_.items():
            self[k] = v

    @staticmethod
    def from_dict(dict_):
        obj = Config()
        for k, v in dict_.items():
            obj[k] = v
        return obj


def create_config(*, model, loss, data, **kwargs):

    now = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
    model_name = f'{data}_{model}_{loss}_{now}'
    history_name = f'{model_name}.csv'
    specs_name = f'{model_name}.json'

    if 'path' in kwargs:
        del kwargs['path']

    # create dictionary with parameters of the experiment
    d = dict(
        model_name=model_name,
        history_file=history_name,
        specs_name=specs_name,
        model=model,
        loss=loss,
        **kwargs)
    config = Config.from_dict(d)

    return config
