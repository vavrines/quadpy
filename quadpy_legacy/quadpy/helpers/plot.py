import math

import numpy

__all__ = ["plot_disks_1d", "plot_disks"]


def plot_disks_1d(plt, pts, weights, total_area):
    """Plot a circles at quadrature points according to weights. The diameters
    sum up to the total area.
    """
    radii = 0.5 * abs(weights) / math.fsum(weights) * total_area
    colors = [
        # use matplotlib 2.0's color scheme
        "#1f77b4" if weight >= 0 else "#d62728"
        for weight in weights
    ]
    _plot_disks_helpers(plt, pts, radii, colors)
    return


def plot_disks(plt, pts, weights, total_area):
    """Plot a circles at quadrature points according to weights.
    """
    flt = numpy.vectorize(float)
    pts = flt(pts)
    weights = flt(weights)
    radii = numpy.sqrt(abs(weights) / math.fsum(weights) * total_area / math.pi)
    colors = [
        # use matplotlib 2.0's color scheme
        "#1f77b4" if weight >= 0 else "#d62728"
        for weight in weights
    ]
    _plot_disks_helpers(plt, pts, radii, colors)
    return


def _plot_disks_helpers(plt, pts, radii, colors):
    for tp, radius, color in zip(pts, radii, colors):
        # highlight circle center
        plt.plot([tp[0]], [tp[1]], linestyle="None", marker=".", color=color)
        # Choose radius such that the sum of areas of the circles equals
        # total_area.
        circ = plt.Circle((tp[0], tp[1]), radius, color=color, alpha=0.5)
        plt.gca().add_artist(circ)
    return


def show_mpl(points, weights, volume, edges, balls=None):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    flt = numpy.vectorize(float)
    points = flt(points)
    weights = flt(weights)

    def plot_spheres(plt, ax, pts, radii, colors):
        h = 1.0e-2

        for tp, r, color in zip(pts, radii, colors):
            # https://matplotlib.org/examples/mplot3d/surface3d_demo2.html
            # Compute sphere for every point anew. This is more costly on the
            # numerical side, but gives the flexibility of drawing sphere of
            # different size with different number of points. Another options
            # would be to precompute x, y, z before the loop, but this can be
            # heavy on the graphics output. See
            # <https://stackoverflow.com/q/45324258/353337>.
            u = numpy.linspace(0, 2 * numpy.pi, int(2 * numpy.pi / h * r) + 1)
            v = numpy.linspace(0, numpy.pi, int(numpy.pi / h * r) + 1)
            _x = numpy.outer(numpy.cos(u), numpy.sin(v))
            _y = numpy.outer(numpy.sin(u), numpy.sin(v))
            _z = numpy.outer(numpy.ones(numpy.size(u)), numpy.cos(v))

            # highlight ball center
            plt.plot(
                [tp[0]], [tp[1]], [tp[2]], linestyle="None", marker=".", color=color
            )

            ax.plot_surface(
                r * _x + tp[0],
                r * _y + tp[1],
                r * _z + tp[2],
                color=color,
                alpha=0.3,
                linewidth=1,
            )

        ax.set_axis_off()
        return

    balls = [] if balls is None else balls

    fig = plt.figure()
    ax = fig.gca(projection=Axes3D.name)
    # ax.set_aspect("equal")
    ax.set_axis_off()

    for edge in edges:
        plt.plot(*edge, color="k", linestyle="-")

    plot_spheres(
        plt,
        ax,
        points,
        # Choose radius such that the sum of volumes of the balls equals
        # total_volume.
        radii=numpy.cbrt(
            abs(weights) / math.fsum(weights) * volume / (4.0 / 3.0 * numpy.pi)
        ),
        colors=["#1f77b4" if weight >= 0 else "#d62728" for weight in weights],
    )

    for ball in balls:
        plot_spheres(plt, ax, [ball[0]], [ball[1]], ["#dddddd"])

    plt.show()
    return


# def show_mayavi(points, weights, volume, edges, balls=None):
#     import mayavi.mlab as mlab
#
#     mlab.figure(bgcolor=(1.0, 1.0, 1.0))
#
#     for edge in edges:
#         mlab.plot3d(*edge, tube_radius=0.5e-2, color=(0.0, 0.0, 0.0))
#
#     blue = (31.0 / 255.0, 119.0 / 255.0, 180.0 / 255.0)
#     red = (84.0 / 255.0, 15.0 / 255.0, 16.0 / 255.0)
#
#     h = 1.0e-2
#     sum_weights = math.fsum(weights)
#     for tp, weight in zip(points, weights):
#         # Choose radius such that the sum of volumes of the balls equals
#         # total_volume.
#         r = (abs(weight) / sum_weights * volume / (4.0 / 3.0 * numpy.pi)) ** (1.0 / 3.0)
#
#         # Create a sphere
#         u = numpy.linspace(0, 2 * numpy.pi, int(2 * numpy.pi / h * r) + 1)
#         v = numpy.linspace(0, numpy.pi, int(numpy.pi / h * r) + 1)
#         sin_u, cos_u = numpy.sin(u), numpy.cos(u)
#         sin_v, cos_v = numpy.sin(v), numpy.cos(v)
#         _x = numpy.outer(cos_u, sin_v)
#         _y = numpy.outer(sin_u, sin_v)
#         _z = numpy.outer(numpy.ones(numpy.size(u)), cos_v)
#
#         mlab.mesh(
#             r * _x + tp[0],
#             r * _y + tp[1],
#             r * _z + tp[2],
#             color=blue if weight >= 0 else red,
#             opacity=1.0,
#         )
#
#     balls = [] if balls is None else balls
#     for ball in balls:
#         tp = ball[0]
#         r = ball[1]
#
#         # Create a sphere
#         u = numpy.linspace(0, 2 * numpy.pi, int(2 * numpy.pi / h * r) + 1)
#         v = numpy.linspace(0, numpy.pi, int(numpy.pi / h * r) + 1)
#         sin_u, cos_u = numpy.sin(u), numpy.cos(u)
#         sin_v, cos_v = numpy.sin(v), numpy.cos(v)
#         _x = numpy.outer(cos_u, sin_v)
#         _y = numpy.outer(sin_u, sin_v)
#         _z = numpy.outer(numpy.ones(numpy.size(u)), cos_v)
#
#         mlab.mesh(
#             r * _x + tp[0], r * _y + tp[1], r * _z + tp[2], color=[0, 0, 0], opacity=1.0
#         )
#
#     mlab.show()
#     return


def show_vtk(points, weights, volume, edges, balls=None, render=True):
    import vtk

    def get_line_actor(x0, x1):
        source = vtk.vtkLineSource()
        source.SetPoint1(x0)
        source.SetPoint2(x1)
        # mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        # actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        # color actor
        actor.GetProperty().SetColor(0, 0, 0)
        return actor

    def get_sphere_actor(x0, r, color, opacity=1.0):
        # Generate polygon data for a sphere
        sphere = vtk.vtkSphereSource()

        sphere.SetCenter(x0)
        sphere.SetRadius(r)

        sphere.SetPhiResolution(100)
        sphere.SetThetaResolution(100)

        # Create a mapper for the sphere data
        sphere_mapper = vtk.vtkPolyDataMapper()
        # sphere_mapper.SetInput(sphere.GetOutput())
        sphere_mapper.SetInputConnection(sphere.GetOutputPort())

        # Connect the mapper to an actor
        sphere_actor = vtk.vtkActor()
        sphere_actor.SetMapper(sphere_mapper)
        sphere_actor.GetProperty().SetColor(color)
        sphere_actor.GetProperty().SetOpacity(opacity)
        return sphere_actor

    flt = numpy.vectorize(float)
    points = flt(points)
    weights = flt(weights)

    balls = [] if balls is None else balls

    line_actors = [get_line_actor(edge[:, 0], edge[:, 1]) for edge in edges]

    blue = numpy.array([31.0, 119.0, 180.0]) / 255.0
    red = numpy.array([84.0, 15.0, 16.0]) / 255.0

    radii = numpy.cbrt(
        abs(weights) / math.fsum(weights) * volume / (4.0 / 3.0 * numpy.pi)
    )
    sphere_actors = [
        get_sphere_actor(pt, radius, color=blue if weight > 0.0 else red)
        for pt, weight, radius in zip(points, weights, radii)
    ]

    sphere_actors.extend(
        [
            get_sphere_actor(
                numpy.array(ball[0]),
                ball[1],
                color=numpy.array([0.0, 0.0, 0.0]) / 255.0,
                opacity=0.5,
            )
            for ball in balls
        ]
    )

    # Create a renderer and add the sphere actor to it
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1.0, 1.0, 1.0)
    for sphere_actor in sphere_actors:
        renderer.AddActor(sphere_actor)
    for line_actor in line_actors:
        renderer.AddActor(line_actor)

    # Create a render window
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    # Create an interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    if render:
        # Initialize the interactor and start the rendering loop
        interactor.Initialize()
        render_window.Render()
        interactor.Start()

    # # Screenshot
    # TODO transparent background
    # w2if = vtk.vtkWindowToImageFilter()
    # w2if.SetInput(render_window)
    # w2if.Update()
    # writer = vtk.vtkPNGWriter()
    # writer.SetFileName('screenshot.png')
    # writer.SetInputConnection(w2if.GetOutputPort())
    # writer.Write()
    return


backend_to_function = {
    # "mayavi": show_mayavi,
    "mpl": show_mpl,
    "vtk": show_vtk,
}
