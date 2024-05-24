import mujoco
import mediapy as media
import matplotlib.pyplot as plt

XML=r"""
<mujoco>
  <asset>
    <mesh file="triangle.stl"/>
  </asset>
  <worldbody>
    <body>
      <freejoint/>
      <geom type="mesh" name="triangle" mesh="triangle"/>
    </body>
  </worldbody>
</mujoco>
"""

ASSETS=dict()
with open('/root/Masters/Sim/revolve2-folding/meshes/triangle.stl', 'rb') as f:
  ASSETS['triangle.stl'] = f.read()

model = mujoco.MjModel.from_xml_string(XML, ASSETS)
renderer = mujoco.Renderer(model, 400, 600)
data = mujoco.MjData(model)
mujoco.mj_forward(model, data)
renderer.update_scene(data, "fixed")
media.show_image(renderer.render())