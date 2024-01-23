from CubeEngine import CubeEngine


cube_engine = CubeEngine(
    screen_width=800,
    screen_height=800,
    unit_px=20,
    dist_factor=0.92,
    size=3
)

cube_engine.game_loop()
