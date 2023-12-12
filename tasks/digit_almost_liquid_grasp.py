from yarok import Platform, PlatformMJC, PlatformHW, component, ConfigBlock, Injector
from yarok.comm.plugins.cv2_waitkey import Cv2WaitKey

from yarok.comm.worlds.empty_world import EmptyWorld
from yarok.comm.components.robotiq_2f85.robotiq_2f85 import Robotiq2f85
from yarok.comm.components.ur5e.ur5e import UR5e
from yarok.comm.components.digit.digit import Digit
from yarok.comm.toys.bucket_particles.bucket_particles import BucketParticles

from yarok.comm.plugins.cv2_inspector import Cv2Inspector

from math import pi


@component(
    extends=EmptyWorld,
    components=[
        UR5e,
        Robotiq2f85,
        Digit,
        BucketParticles
    ],
    # language=xml
    template="""
        <mujoco>
            <worldbody>
                <bucket-particles name="bucket"/>
                <body name="base-table" pos='-0.135 -0.48 0.016'>
                    <geom type='box' size='0.2 0.2 0.13'/>
                </body>

                <ur5e name="arm"> 
                   <robotiq-2f85 name="gripper" parent="ee_link"> 
                        <body xyaxes='0 0 -1 1 0 0' pos="-0.001  0.009 .064" parent='right_tip'>
                            <digit name="digit1" />
                        </body>
                        <body xyaxes='0 0 -1 1 0 0' pos="-0.001  0.009 .064" parent='left_tip'>
                            <digit name="digit2" />
                        </body>
                    </robotiq-2f85> 
                </ur5e>  
            </worldbody>        
        </mujoco>
    """
)
class AlmostLiquidWorld:
    pass


class AlmostLiquidPouringBehaviour:

    def __init__(self, pl: Platform, injector: Injector):
        self.arm: UR5e = injector.get('arm')
        self.gripper = injector.get('gripper')
        self.pl = pl

    def on_update(self):
        # self.pl.wait_seconds(60)
        # print('------------------------------------------------------------------------------------------->')

        q = [0, -pi / 2, -pi / 2 + pi / 4, 0, pi / 2, pi / 2]
        self.arm.move_q(q)
        self.gripper.move(0)
        self.pl.wait(lambda: self.arm.is_at(q) and self.gripper.is_at(0))
        print('----')

        q = [0, -pi / 2, -pi / 2, -pi / 2, pi / 2, pi / 2]
        self.arm.move_q(q)
        self.pl.wait(lambda: self.arm.is_at(q))
        print('----')

        # self.gripper.move(0.78)

        # self.pl.wait_seconds(10)

        q = [0, -pi / 2, - pi / 2 - pi / 10, -pi / 2 + pi / 10, pi / 2, pi / 2]
        self.arm.move_q(q)

        self.pl.wait(lambda: self.arm.is_at(q))
        self.pl.wait_seconds(3)

        self.pl.wait_seconds(5)
        self.gripper.move(235)
        # self.pl.wait(lambda: self.gripper.is_at(200))
        self.pl.wait_seconds(3)

        q = [0, -pi / 2, - pi / 2 - pi / 10 + pi / 5, -pi / 2 + pi / 10 - pi / 5, pi / 2, pi / 2]
        self.arm.move_q(q)
        self.pl.wait(lambda: self.arm.is_at(q))

        q = [0, -pi / 2, -pi / 2 + pi / 4, 0, pi / 2, pi / 2]
        self.arm.move_q(q)
        self.pl.wait(lambda: self.arm.is_at(q))


def digit_almost_liquid_grasp():
    conf = {
        'world': AlmostLiquidWorld,
        'behaviour': AlmostLiquidPouringBehaviour,
        'defaults': {
            'environment': 'sim',
            'components': {
                '/gripper': {
                    'left_tip': False,
                    'right_tip': False,
                }
            },
            'plugins': [
                (Cv2Inspector, {}),
                (Cv2WaitKey, {}),
            ]
        },
        'environments': {
            'sim': {
                'platform': {
                    'class': PlatformMJC,
                    'width': 1000,
                    'height': 800,
                }
            }
        },
    }
    Platform.create(conf).run()


if __name__ == '__main__':
    digit_almost_liquid_grasp()
