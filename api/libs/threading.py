def apply_gevent_threading_patch():
    """
    Run threading patch by gevent when DEBUG mode enabled
    to make standard library threading compatible.
    Patching should be done as early as possible in the lifecycle of the program.
    :return:
    """
    import grpc.experimental.gevent
    from gevent import monkey

    monkey.patch_all()
    grpc.experimental.gevent.init_gevent()
