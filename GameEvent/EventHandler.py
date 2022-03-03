# -*- coding: UTF-8 -*-

from GameEvent import Event


class EventHandlerBase(object):

	def __init__(self):
		self._event = Event.EventDispacther()

	def reg_event(self, event_id, fun, ord=1000):
		self._event.reg_event(event_id, fun, ord)

	def trigger_event(self, event_id, *params, **kwargs):
		self._event.trigger_event(event_id, *params, **kwargs)