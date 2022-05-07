from manim import *

class ConfigurationSpace(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        self.camera.frame.scale(0.5).move_to(LEFT*4+UP*0.5)
        def line_intersection(line1, line2):
            x1 = line1[0][0]
            x2 = line1[0][1]
            x3 = line2[0][0]
            x4 = line2[0][1]

            y1 = line1[1][0]
            y2 = line1[1][1]
            y3 = line2[1][0]
            y4 = line2[1][1]

            paramt=False

            if ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4)) * ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)) > 0 and abs((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)) >= abs((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4)):
                paramt=True

            if abs((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)) >= abs((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2)) and ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)) * ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2)) > 0 and paramt:
                return True

            return False

        def createObstacle(color,position):
            obstacle=Square(color=color, fill_opacity=0.5,side_length=0.5)
            obstacle.move_to(position)
            self.play(Create(obstacle))
            return obstacle

        def createRobot():
            line1 = Line(LEFT*3,LEFT*4)
            line2 = Line(LEFT*4, LEFT*3)
            line2_ref = line2.copy()
            line2.rotate(
                theta1_tracker.get_value() * DEGREES, about_point=line2.get_start()
            )
            
            line3 = Line(line2.get_end(),line2.get_start())
            line3_ref = line3.copy()
            line3.rotate(
                theta2_tracker.get_value() * DEGREES, about_point=line3.get_start()
            )
            
            
            a1 = Angle(line1, line2,quadrant=(-1,1),radius=0.3, other_angle=False,color=YELLOW)
            tex1 = MathTex(r"\theta_1",color=YELLOW).move_to(
                Angle(
                    line1, line2, radius=0.3 + 3 * SMALL_BUFF,quadrant=(-1,1),other_angle=False
                ).point_from_proportion(0.5)
            )
            
            a2 = Angle(line2, line3,quadrant=(-1,1),radius=0.3, other_angle=False)
            tex2 = MathTex(r"\theta_2", color=BLUE).move_to(
                Angle(
                    line2, line3, radius=0.3 + 3 * SMALL_BUFF,quadrant=(-1,1),other_angle=False
                ).point_from_proportion(0.5)
            )
            robot = VGroup(line2 ,line3, a1, a2, tex1, tex2)
            self.add(robot)
            line2.add_updater(
                lambda x: x.become(line2_ref.copy()).rotate(
                    theta1_tracker.get_value() * DEGREES, about_point=line2.get_start()
                ) 
            )
            line3.add_updater(
                lambda x: x.become(line2_ref.copy()).rotate(
                    theta1_tracker.get_value() * DEGREES, about_point=line2.get_start()
                ).rotate(
                    180 * DEGREES,about_point=line2.get_center()
                ).rotate( 
                    theta2_tracker.get_value() * DEGREES, about_point=line2.get_end()
                    )
            )
            a1.add_updater(
                lambda x: x.become(Angle(line1, line2,quadrant=(-1,1), radius=0.3, color=YELLOW, other_angle=False))
            )
            tex1.add_updater(
                lambda x: x.move_to(
                    Angle(
                        line1, line2,quadrant=(-1,1), radius=0.3 + 3 * SMALL_BUFF, other_angle=False
                    ).point_from_proportion(0.5)
                )
            )
            a2.add_updater(
                lambda x: x.become(Angle(line2, line3,quadrant=(-1,1), radius=0.3,color=BLUE, other_angle=False))
            )
            tex2.add_updater(
                lambda x: x.move_to(
                    Angle(
                        line2, line3,quadrant=(-1,1), radius=0.3 + 3 * SMALL_BUFF, other_angle=False
                    ).point_from_proportion(0.5)
                )
            )
            return robot

        def collisionChecker(line2,line3,obstacle_id):
            line1 = [[line2.get_end()[0],line2.get_start()[0]],[line2.get_end()[1],line2.get_start()[1]]]
            line2 = [[line3.get_end()[0],line3.get_start()[0]],[line3.get_end()[1],line3.get_start()[1]]]
            
            obsx = obstacles[obstacle_id].get_center()[0]
            obsy = obstacles[obstacle_id].get_center()[1]
            obsline1 = [[obsx-0.25,obsx-0.25],[obsy-0.25,obsy+0.25]]
            obsline2 = [[obsx-0.25,obsx+0.25],[obsy+0.25,obsy+0.25]]
            obsline3 = [[obsx+0.25,obsx+0.25],[obsy-0.25,obsy+0.25]]
            obsline4 = [[obsx-0.25,obsx+0.25],[obsy-0.25,obsy+0.25]]
            
            #check obstacle line 1
            if line_intersection(line1,obsline1):
                return obstacle_id+1
            if line_intersection(line1,obsline2):
                return obstacle_id+1
            if line_intersection(line1,obsline3):
                return obstacle_id+1
            if line_intersection(line1,obsline4):
                return obstacle_id+1


            #check obstacle line2
            if line_intersection(line2,obsline1):
                return obstacle_id+1
            if line_intersection(line2,obsline2):
                return obstacle_id+1
            if line_intersection(line2,obsline3):
                return obstacle_id+1
            if line_intersection(line2,obsline4):
                return obstacle_id+1

            return 0

        def createConfigurationSpace():            
            axes = NumberPlane(
                x_length=6,
                y_length=6,
                x_range = [0, 360, 10],
                y_range = [0, 360, 10],
                background_line_style={
                    "stroke_color": TEAL,
                    "stroke_width": 0.5,
                    "stroke_opacity": 0.6
                },
                axis_config={
                    "include_numbers": False,
                    "numbers_to_include": np.arange(0, 360, 90),
                    "numbers_with_elongated_ticks": np.arange(0, 360, 90)
                    },
                tips=False
            )
            
            theta1_graph = axes.plot_line_graph(
                x_values = [0, theta1_tracker.get_value()],
                y_values = [theta2_tracker.get_value(),theta2_tracker.get_value()],
                line_color=YELLOW,
            # vertex_dot_style=dict(stroke_width=3,  fill_color=PURPLE),
                stroke_width = 4,
            )

            theta1_graph.add_updater(
                lambda x: x.become(axes.plot_line_graph(
                x_values = [0, theta1_tracker.get_value()],
                y_values = [theta2_tracker.get_value(),theta2_tracker.get_value()],
                line_color=YELLOW,
            # vertex_dot_style=dict(stroke_width=3,  fill_color=PURPLE),
                stroke_width = 4,
            ))
            )

            theta2_graph = axes.plot_line_graph(
                x_values = [theta1_tracker.get_value(), theta1_tracker.get_value()],
                y_values = [theta2_tracker.get_value(),0],
                line_color=BLUE,
                stroke_width = 4,
            )

            theta2_graph.add_updater(
                lambda x: x.become(axes.plot_line_graph(
                x_values = [theta1_tracker.get_value(), theta1_tracker.get_value()],
                y_values = [theta2_tracker.get_value(),0],
                line_color=BLUE,
                stroke_width = 4,
            ))
            )


            plot = VGroup(axes, theta1_graph, theta2_graph)
            plot.move_to([3,0,0])
            self.play(Create(plot))
            return plot

        def createObstacleSpace(plot,obstacle_id):
            for theta1 in range(1,36,1):
                for theta2 in range(1,36,1):
                
                    line2_temp = Line(LEFT*4, LEFT*3)
                    line2_temp.rotate(
                        theta1 * 10 * DEGREES, about_point=line2_temp.get_start()
                    )
                
                    line3_temp = Line(line2_temp.get_end(),line2_temp.get_start())
                    line3_temp.rotate(
                        theta2 * 10 * DEGREES, about_point=line3_temp.get_start()
                    )

                    collision = collisionChecker(line2_temp,line3_temp,obstacle_id)
                    color = {
                        1 : PINK,
                        2 : RED,
                        3 : YELLOW_C
                    }
                    if collision>0:
                        dot = Square(color=color.get(collision), fill_opacity=1,side_length=0.13).move_to(plot[0].coords_to_point(theta1*10, theta2*10)+0.08)
                        dot.z_index=-1
                        self.add(dot)



        theta1_tracker = ValueTracker(90)
        theta2_tracker = ValueTracker(181)
       
       

        
        robot = createRobot()
        self.wait(2)
        self.play(theta1_tracker.animate.set_value(270))
        self.play(theta1_tracker.animate.set_value(40))
        self.play(theta1_tracker.animate.set_value(90))
        self.play(theta2_tracker.animate.set_value(90))
        self.play(theta2_tracker.animate.set_value(270))
        self.play(theta2_tracker.animate.set_value(181))
        self.wait(2)

        self.play(Restore(self.camera.frame))
        configurationSpace  = createConfigurationSpace()
        
        self.wait(1)
        self.play(theta1_tracker.animate.set_value(270))
        self.play(theta1_tracker.animate.set_value(40))
        self.play(theta1_tracker.animate.set_value(90))
        self.play(theta2_tracker.animate.set_value(90))
        self.play(theta2_tracker.animate.set_value(270))
        self.play(theta2_tracker.animate.set_value(181))


        self.play(theta1_tracker.animate.set_value(200))

        obstacles           = VGroup()
        obstacles.add(createObstacle(PINK,[-2, 0, 0]))
        obstacleSpace0       = createObstacleSpace(configurationSpace,0)
        self.wait(1)
        obstacles.add(createObstacle(RED,[-4, 1, 0]))
        obstacleSpace1       = createObstacleSpace(configurationSpace,1)
        self.wait(1)
        obstacles.add(createObstacle(YELLOW_C,[-3, -1, 0]))
        obstacleSpace2       = createObstacleSpace(configurationSpace,2)
        self.wait(3)
        
        self.play(theta1_tracker.animate.set_value(250),theta2_tracker.animate.set_value(340))
        self.play(theta1_tracker.animate.set_value(320),theta2_tracker.animate.set_value(270))
        self.play(theta1_tracker.animate.set_value(340),theta2_tracker.animate.set_value(190))
        self.play(theta1_tracker.animate.set_value(360),theta2_tracker.animate.set_value(135))
        theta1_tracker.set_value(1)
        self.play(theta1_tracker.animate.set_value(60),theta2_tracker.animate.set_value(90))
        self.play(theta2_tracker.animate.set_value(181))
        
        self.wait(10)