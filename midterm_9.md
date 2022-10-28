# Ethics of Robotics:

# A
The assumption that any field can be wholly devoid of ethics is foolhardy. Robotics inherently will be used in unethical ways, and researchers should be aware of this. While ignoring ethics may allow for faster development and easier sales, it will inevitably be costly in some form or another. All progress can be used for good and bad, and we have a responsibility to do the best we can to limit the harm that can be done by our work, regardless of the field.

# B
The laws of robotics are oversimplifications of a complex field, and don’t even scratch the surface of implementation. Each law is algorithmically complex beyond almost anything we have developed today. What constitutes a human being? What does it mean to do harm? Does every robot have to have functions to prevent harm in order to avoid inaction? The first law alone assumes that a robot thinks and understands like we do. It assumes an innate understanding of things that not even all humans fully understand. The second law is not much better. Which humans does it listen to? All of them? Again, what constitutes harm? Does being told to work contrary to the robot's purpose harm someone by not fulfilling the original design of the robot? The third law makes an assumption that all robots are built to last, and that they understand what it means to protect itself. None of these questions or concepts are algorithmically simple. None of them are easily “taught” to a robot.

An example of this could be self driving cars. An oversimplification via pseudo code may look something like this

```
While driving:
    If the path is blocked:
        If there is time to stop
            Stop
        Otherwise,
            If the obstacle big enough to cause harm to a passenger:
                If swerving hurt someone else:
                    Choose between the passenger and the other person
                    based on goal to minimize harm
                Else
                    Swerve
            Else:
                If I can prevent harm to myself without hurting someone else:
        Swerve
Else:
    Hit the obstacle, minimize damage
Else:
    Follow path
If the driver wants to take control:
    Switch to driver control mode
```

# C
It is interesting to me that there isn’t a system of liability already implemented with the direction that autonomous vehicles have been going. Unfortunately we may need more incidents like the one in Tempe before this is well regulated. In my opinion, like what is alluded to in the wiki page, in any case where a driver was not controlling the vehicle (level 5), the manufacturer should always be liable unless another third party caused the damage (someone hit the vehicle). When the driver and vehicle share control, it becomes much more complex. If something in the autonomous system is defective, it makes sense that the manufacturer would be held liable for a shared-control crash. Otherwise, blame could likely be placed on the driver.

# D
Regulating autonomous systems is complex because of the large variety that exists in the field. A good baseline would be holding the creator of an autonomous system accountable for any damage caused by the system while acting entirely autonomously. If someone dies in an accident and an autonomous system is entirely responsible, that may mean manslaughter charges for the designer. 

If proper warnings were given, and the robot was operating as expected, it could be the fault of the owner for not providing a safe workspace for the system, or posting warnings as instructed by the manufacturer.

Any laws that place restrictions on technology risk limiting technological advancement, or useful application, in that area. It takes time, money, and effort to comply with regulations. The risk of causing harm with an autonomous system may be large enough that some companies or developers stay completely out of the field of automation.




