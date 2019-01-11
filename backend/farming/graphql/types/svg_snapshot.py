import os
from promise import Promise
from promise.dataloader import DataLoader
import requests


class SVGSnapshotLoader(DataLoader):
    def batch_load_fn(self, lpis_parcel_ids):
        svgs = []
        for lpis_parcel_id in lpis_parcel_ids:
            url = os.getenv('FAST_API_PARCEL_SNAPSHOT_SVG_URL')
            payload = {'primary': lpis_parcel_id[0], 'secondary': lpis_parcel_id[1]}
            svg = requests.post(url, json=payload).text
            svgs += [svg]

        return Promise.resolve(svgs)


svg_snapshot_loader = SVGSnapshotLoader()
