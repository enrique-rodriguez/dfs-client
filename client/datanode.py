from client.utils import HttpService




class DataNode(HttpService):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id

    @classmethod
    def from_json(cls, obj):
        return cls(
            obj.get("id"),
            obj.get("host"),
            obj.get("port"),
        )

    def is_active(self):
        try:
            res = super().get(f"/health")
        except self.exception_class:
            return False

        return res.status_code == 200

    def put(self, block):
        res = self.post(f"/blocks", files={"block": block.content})

        block.id = res.json().get("id")
        block.datanode_id = self.id

    def get(self, blockid):
        res = super().get(f"/blocks/{blockid}")
        return res.content
