from gibson2.robots.robot_locomotors import Turtlebot
from gibson2.core.simulator import Simulator
from gibson2.scenes.scene import BuildingScene
from gibson2.objects.base_object import YCBObject
from gibson2.utils.utils import parse_config
import numpy as np
from gibson2.core.render.profiler import Profiler


def main():
    config = parse_config('../configs/turtlebot_demo.yaml')
    s = Simulator(mode='gui', image_width=256, image_height=256, enable_shadow=True, enable_msaa=False)

    scene = BuildingScene('Rs',
                          build_graph=True,
                          pybullet_load_texture=True)
    s.import_scene(scene)
    turtlebot = Turtlebot(config)
    s.import_robot(turtlebot)

    for _ in range(10):
        obj = YCBObject('003_cracker_box')
        s.import_object(obj)
        obj.set_position_orientation(np.random.uniform(low=0, high=2, size=3), [0,0,0,1])

    print(s.renderer.instances)

    for item in s.renderer.instances[1:]:
        item.use_pbr = True
        item.use_pbr_mapping = False
        item.metalness = np.random.random()
        item.roughness = np.random.random()

    for i in range(10000):
        with Profiler('Simulator step'):
            turtlebot.apply_action([0.1,0.1])
            s.step()
            rgb = s.renderer.render_robot_cameras(modes=('rgb'))

    s.disconnect()


if __name__ == '__main__':
    main()
