# Character editor

Данный проект реализует модуль внутриигрового редактора персонажа с поддержкой системы захвата движений головы и мимики лица игрока в реальном времени .

## System capabilities

This system implements the following main functions:

- creation of save slots;
- overwriting save slots;
- removal of save slots;
- loading save slots;
- control of morphing parameters of the game character for individual body parts;
- the choice of the model of the game character;
- the choice of clothes for the game character for different parts of the body;
- the choice of animations of the game character for various parts of the body;
- the choice of animations of the game character for various states;
- three-dimensional three-dimensional reconstruction of the player's face (prototype);
- testing a game character at a game location;
- transition between logical levels of the system with the ability to save the changes made by the user.

<img src="./_documentation/levels_system.png?raw=true" width=450px height="auto" />

## System architecture

<img src="./_documentation/architecture.png?raw=true" width=450px height="auto" />

## 3D-reconstruction model

<img src="./_documentation/3d_reconstruction.png?raw=true" width=600px height="auto" />

## Model motion capture head and facial expressions of the player

<img src="./_documentation/motion_capture.png?raw=true" width=600px height="auto" />

## Development tools

| Tool                   | Basic plugins / libraries / frameworks | Plugin / Library / Framework Purpose                                                                                                           |
| :--------------------- | :------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| **Unreal Engine 4.26** | SocetIO-Client-UE4                     | Allows you to organize the logic of a UDP client.                                                                                              |
|                        | UnrealAnimatedTexturePlugin            | Allows you to import animated textures into UE 4 and use them in your own project.                                                             |
|                        | MixamoConverter                        | An extension for converting animations received through Mixamo to a format suitable for use in the UE 4.                                       |
| **Daz 3D 4.15**        | Genesis 8                              | A package of 3D models of humanoid characters of the eighth generation.                                                                        |
|                        | DazToUnreal                            | A plug-in that provides the ability to correctly export three-dimensional character models from the Daz 3D environment to the Unreal Engine 4. |
| **Python**             | Mediapipe                              | A framework that allows you to solve the problems of building a facial mesh, face tracking, object recognition and tracking, and much more.    |
|                        | PyQt5                                  | Allows to form and display interfaces for programs written in the Python programming language.                                                 |
|                        | Socet                                  | Allows you to organize the logic of a UDP server.                                                                                              |
| **Mixamo**             | -                                      | Allows to create sets of animations for three-dimensional models of a game character.                                                          |

## Demonstration of work

### Video demonstration

[<img src="./_documentation/che_main_menu.png?raw=true" width=600px height="auto" style="border: 1px solid gray"/>](https://www.youtube.com/watch?v=tpZt8SZ9sSQ)

### Create/Save/load session CE

<img src="./_documentation/che_ls.png?raw=true" width=600px height="auto" style="border: 1px solid gray"/>

### Main interfere CE

<img src="./_documentation/che_mi.png?raw=true" width=600px height="auto" style="border: 1px solid gray"/>

### Testing mode CE

<img src="./_documentation/che_ti.png?raw=true" width=600px height="auto" style="border: 1px solid gray"/>

### Data acquisition panel for 3D reconstruction and motion capture CE

<img src="./_documentation/che_settings.png?raw=true" width=300px height="auto" style="border: 1px solid gray"/>

### Motion capture system on Python

<img src="./_documentation/che_fd.png?raw=true" width=350px height="auto" style="border: 1px solid gray"/>
