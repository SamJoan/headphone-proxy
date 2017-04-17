from collections import OrderedDict

class DisplayFlow():
    host = ""
    method = ""
    path = ""
    status_code = ""
    length = 0
    has_cookies = None
    port = 0
    scheme = ""
    time_requested = ""

    @staticmethod
    def cols():
        return [x.title() for x in DisplayFlow.__dict__.keys() if '_' not in x and not x == 'cols']

class State():
    instance = None
    flows = OrderedDict()
    # Provides o(1) lookups
    flow_to_row = {}

    def add_flow(self, flow, row_id):
        self.flows[flow.id] = flow
        self.flow_to_row[flow.id] = row_id

    def update_flow(self, flow):
        self.flows[flow.id] = flow
        return self.flow_to_row[flow.id]

    @staticmethod
    def get():
        if not State.instance:
            State.instance = State()

        return State.instance
