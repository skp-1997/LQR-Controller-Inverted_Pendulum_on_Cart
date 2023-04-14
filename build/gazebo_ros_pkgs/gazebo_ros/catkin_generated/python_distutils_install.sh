#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/ses598/ros_ws/src/gazebo_ros_pkgs/gazebo_ros"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/ses598/ros_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/ses598/ros_ws/install/lib/python3/dist-packages:/home/ses598/ros_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/ses598/ros_ws/build" \
    "/usr/bin/python3" \
    "/home/ses598/ros_ws/src/gazebo_ros_pkgs/gazebo_ros/setup.py" \
     \
    build --build-base "/home/ses598/ros_ws/build/gazebo_ros_pkgs/gazebo_ros" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/ses598/ros_ws/install" --install-scripts="/home/ses598/ros_ws/install/bin"
