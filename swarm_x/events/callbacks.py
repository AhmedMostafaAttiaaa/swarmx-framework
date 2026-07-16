def on_handoff(bus, callback): return bus.subscribe("handoff", callback)
def on_tool_call(bus, callback): return bus.subscribe("tool_started", callback)
def on_error(bus, callback): return bus.subscribe("error", callback)

