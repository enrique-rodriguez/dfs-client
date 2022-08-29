import json
from client import file
from client.utils import HttpService
from client.datanode import DataNode


class MetaData(HttpService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.datanodes = dict()

    def list_nodes(self):
        res = super().get("/datanodes")

        return [DataNode.from_json(obj) for obj in res.json()]

    def list_files(self):
        res = super().get("/files")

        return [file.File.from_json(f) for f in res.json()]
    
    def delete(self, file_id):
        res = super().delete(f"/files/{file_id}")

    def add_file(self, file):
        data = {"name": file.name, "size": file.size}
        res = super().post(f"/files", data=data)
        file.id = res.json().get("id")

    def get_file(self, file_id, include_blocks=False):
        res = super().get(f"/files/{file_id}")
        if res.status_code == 404:
            return None
        fobj = res.json()
        if include_blocks:
            self.include_blocks(file_id, fobj)
        return file.File.from_json(fobj)

    def add_blocks_for(self, file):
        blocks = [{"id": b.id, "datanode_id": b.datanode_id} for b in file.blocks]
        b = json.dumps(blocks)
        data = {"blocks": b}
        super().post(f"/files/{file.id}/blocks", data=data)

    def include_blocks(self, file_id, fobj, cache_nodes=True):
        self.clear_datanodes()
        res = super().get(f"/files/{file_id}/blocks")
        blocks = res.json()
        fobj["blocks"] = []
        for block in blocks:
            fobj["blocks"].append(file.Block.from_json(block))
            if not cache_nodes:
                continue
            self.cache_datanode(block["datanode"])

    def clear_datanodes(self):
        self.datanodes.clear()

    def cache_datanode(self, datanode):
        dnode_id = datanode["id"]
        if dnode_id in self.datanodes:
            return
        self.datanodes[dnode_id] = DataNode.from_json(datanode)