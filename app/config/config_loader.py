import yaml


class Config:
    def __init__(self):
        with open("config.yaml") as f:
            self.data = yaml.safe_load(f)

    def get_channels(self):
        return self.data.get('channels', [])

    def is_reaction_enabled(self, channel_id):
        return self.data['reactions'].get(str(channel_id), False)


config = Config()