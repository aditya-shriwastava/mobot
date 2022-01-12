import mobot
from mobot_utils.image_grid import ImageGrid

import torch
import torchvision

import numpy as np
import time

class PersonFollowerAgent(mobot.Agent):
    def __init__(self):
        super().__init__()
        self.image_grid = ImageGrid(self)
        self.camera.register_callback(self.camera_cb)

        self.model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_320_fpn(pretrained=True)
        self.model.eval()

    def camera_cb(self, img, meta):
        start = time.time()

        img_tensor = torch.tensor(img.copy()).permute(2,0,1)
        predictions = self.model(
            img_tensor.to(torch.float32).unsqueeze(0)/255
        )[0]

        index = torch.logical_and(
            predictions['labels'] == 1,
            predictions['scores'] >= 0.9
        )

        if index.any():
            bbox = predictions['boxes'][index][0]
            score = "{:.2f}".format(predictions['scores'][index][0])
            img_disp = torchvision.utils.draw_bounding_boxes(
              img_tensor,
              bbox.unsqueeze(0),
              labels=[f'Person: {score}'],
              colors=(255,0,0))
            self.image_grid.new_image(np.array(img_disp.permute(1,2,0)))
        else:
            self.image_grid.new_image(img)

        print(f"dt: {time.time() - start}")


person_follower_agent = PersonFollowerAgent()
person_follower_agent.start()

