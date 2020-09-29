import json
import math
import random
import re
import traceback
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum

# import requests
# from background_task import background
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Max

# from api import sms, email_api
# from api.binance_api import Binance, get_non_scientific_value, BinanceOrderSide, OcoStatus
# from api.binance_future_api import BinanceFuture
# from api.bitmex_api import Bitmex
# from api.exceptions import *
# from api.redis import Redis
# from oms.enums import Side
# from telegram_bot.generic_utils import BotNotification
# from trade import log, settings
# from trade.settings import MAX_TIMEOUT_PRICE, unique_order_id_concat, MAX_ACTIVE_TRADES_ON_SYMBOL, \
#     MAX_TIMEOUT_ORDER, MAX_PRICE_DEVIATION, MAX_ORDERS_PER_TRADE, PRACTICAL_MIN_NOTIONAL_INDEX, MIN_PRICE_DEVIATION, \
#     MAX_TIMEOUT_BIN_1_MIN, MAX_TIMEOUT_ORDER_BINANCE, unique_list_id_concat, bot_address, bot_address_future, \
#     spot_bot_token, future_bot_token, bot_token

#
# def are_equal(value1, value2=0, abs_tol=9e-9, rel_tol=None):
#     if value1 is None:
#         value1 = 0
#     if value2 is None:
#         value2 = 0
#     if rel_tol is not None:
#         return math.isclose(float(value1), float(value2), rel_tol=float(rel_tol))
#     return math.isclose(float(value1), float(value2), abs_tol=float(abs_tol))
#
#
# def str_to_float_array(string, already_normal=False):
#     if already_normal:
#         array = [float(s) for s in string.split(', ')]
#     else:
#         array = [float(s) for s in re.split('-|,| ', string) if s.replace('.', '', 1).isdigit()]
#     # array = [Decimal(s) for s in re.split('-|,| ', string) if s.replace('.', '', 1).isdigit()]
#     # targets = [float(s) for s in str_targets.split('-') if s.isdigit()]
#     if len(array) < 1:
#         raise ValueError("Unable to decipher str: %s" % string)
#     return array
#
#
# def array_to_str(array):
#     array = [get_non_scientific_value(num) for num in array]
#     return ", ".join(map(str, array))
#
#
# class TraceException(Exception):
#     pass
#
#
# def summarize_log(text):
#     if text is None:
#         return False, None
#     MAX_LINES = 5000
#     HEAD_LINES = 1000
#     TAIL_LINES = 1000
#     lines = text.splitlines()
#     if lines.__len__() > MAX_LINES:
#         head = lines[0:HEAD_LINES]
#         tail = lines[-TAIL_LINES:]
#         head = "\n".join(head)
#         tail = "\n".join(tail)
#         msg = log.info("Summarized...", should_print=False)
#         between = "\n\n %s\n\n" % msg
#         return True, head + between + tail
#     else:
#         return False, None
#
#         # head = text[0:HEAD_LINES * CHARS_PER_LINE]
#         # tail = text[-TAIL_LINES * CHARS_PER_LINE:]
#
#
# class StrategyType(Enum):
#     TRAIL_TARGETS_WITH_MARKET = 1
#     TRAIL_NO_TARGETS_WITH_LIMIT = 4
#     TRAIL_TARGETS_WITH_LIMIT = 5
#     NO_TARGETS_WITH_MARKET = 6
#     TAKE_PROFIT_ON_TARGET = 7
#     TAKE_PROFIT_OCO = 8
#
#     PRICE_FOLLOWER = 2
#     MULTIPLE_TRAIL = 3
#
#
# class Position(Enum):
#     SHORT = 1
#     LONG = 2
#
#     @staticmethod
#     def choices():
#         return (
#             (Position.SHORT.value, Position.SHORT.name),
#             (Position.LONG.value, Position.LONG.name),
#         )
#
#     @staticmethod
#     def get_opposite(position):
#         if position == Position.SHORT.value:
#             return Position.LONG.value
#         if position == Position.LONG.value:
#             return Position.SHORT.value
#         raise ValueError(f"Position must be SHORT or LONG ({Position.SHORT.value} or {Position.LONG.value})")
#
#     def __str__(self):
#         if self.value == 1:
#             return "SHORTTT "
#         if self.value == 2:
#             return "LONGGG "
#         raise ValueError(f"Position must be SHORT or LONG ({Position.SHORT.value} or {Position.LONG.value})")
#
#     @staticmethod
#     def get_string(position):
#         if position == Position.SHORT.value:
#             return "SHORT"
#         if position == Position.LONG.value:
#             return "LONG"
#         raise ValueError(f"Position must be SHORT or LONG ({Position.SHORT.value} or {Position.LONG.value})")
#
#
# class OrderState(Enum):
#     WAITING = 1
#     RUNNING = 2
#     FINISHED = 3
#     CANCELED = 4
#     ERROR = 5
#     EXPIRED = 6
#
#     @staticmethod
#     def get_active_states():
#         return [OrderState.WAITING.value, OrderState.RUNNING.value]
#
#     @staticmethod
#     def get_string(state):
#         if state == OrderState.WAITING.value:
#             return OrderState.WAITING.name
#         if state == OrderState.RUNNING.value:
#             return OrderState.RUNNING.name
#         if state == OrderState.FINISHED.value:
#             return OrderState.FINISHED.name
#         if state == OrderState.CANCELED.value:
#             return OrderState.CANCELED.name
#         if state == OrderState.ERROR.value:
#             return OrderState.ERROR.name
#         if state == OrderState.EXPIRED.value:
#             return OrderState.EXPIRED.name
#
#
# class TradeState(Enum):
#     WAITING = 1
#     ENTERING = 7
#     ENTERED = 2
#     EXITING = 3
#     FINISHED = 4
#     CANCELED = 5
#     CANCELING = 6
#     IDLE = 8
#
#     @staticmethod
#     def get_active_states():
#         return [TradeState.WAITING.value,
#                 TradeState.ENTERING.value,
#                 TradeState.ENTERED.value]
#
#     @staticmethod
#     def get_string(state):
#         if state == TradeState.WAITING.value:
#             return TradeState.WAITING.name
#         if state == TradeState.ENTERING.value:
#             return TradeState.ENTERING.name
#         if state == TradeState.ENTERED.value:
#             return TradeState.ENTERED.name
#         if state == TradeState.EXITING.value:
#             return TradeState.EXITING.name
#         if state == TradeState.FINISHED.value:
#             return TradeState.FINISHED.name
#         if state == TradeState.CANCELED.value:
#             return TradeState.CANCELED.name
#         if state == TradeState.CANCELING.value:
#             return TradeState.CANCELING.name
#         if state == TradeState.IDLE.value:
#             return TradeState.IDLE.name
#
#
# # class OldOrderType(Enum):
# #     Bitmex_market_order = 1
# #     Bitmex_stop_market_order = 2
# #     Binance_market_order = 3
# #     Binance_stop_market_order = 4
# #     Binance_Virtual_stop_order = 5
#
#
# class OrderType(Enum):
#     MARKET = 1
#     STOP_MARKET = 2
#     LIMIT = 3
#     VIRTUAL_STOP_Market = 4
#     VIRTUAL_STOP_LIMIT = 5
#     STOP_LIMIT = 6
#
#     @staticmethod
#     def get_real_order_types():
#         return [
#             OrderType.MARKET.value,
#             OrderType.STOP_MARKET.value,
#             OrderType.LIMIT.value,
#             OrderType.STOP_LIMIT.value,
#         ]
#
#
# class AutoTradeCreatorType(Enum):
#     Number = 1
#     # Percentage = 2
#
#
# class Choices:
#     trade_strategy_type = (
#         (StrategyType.TRAIL_TARGETS_WITH_MARKET.value, StrategyType.TRAIL_TARGETS_WITH_MARKET.name),
#         (StrategyType.TRAIL_NO_TARGETS_WITH_LIMIT.value, StrategyType.TRAIL_NO_TARGETS_WITH_LIMIT.name),
#         (StrategyType.TRAIL_TARGETS_WITH_LIMIT.value, StrategyType.TRAIL_TARGETS_WITH_LIMIT.name),
#         (StrategyType.NO_TARGETS_WITH_MARKET.value, StrategyType.NO_TARGETS_WITH_MARKET.name),
#         (StrategyType.TAKE_PROFIT_ON_TARGET.value, StrategyType.TAKE_PROFIT_ON_TARGET.name),
#         (StrategyType.TAKE_PROFIT_OCO.value, StrategyType.TAKE_PROFIT_OCO.name),
#
#         (StrategyType.PRICE_FOLLOWER.value, StrategyType.PRICE_FOLLOWER.name),
#         (StrategyType.MULTIPLE_TRAIL.value, StrategyType.MULTIPLE_TRAIL.name),
#     )
#
#     auto_trade_creator_type = (
#         (AutoTradeCreatorType.Number.value, AutoTradeCreatorType.Number.name),
#         # (AutoTradeCreatorType.Percentage.value, AutoTradeCreatorType.Percentage.name),
#     )
#
#     order_state_choices = (
#         (OrderState.WAITING.value, OrderState.WAITING.name),
#         (OrderState.RUNNING.value, OrderState.RUNNING.name),
#         (OrderState.FINISHED.value, OrderState.FINISHED.name),
#         (OrderState.CANCELED.value, OrderState.CANCELED.name),
#         (OrderState.ERROR.value, OrderState.ERROR.name),
#         (OrderState.EXPIRED.value, OrderState.EXPIRED.name),
#         # (4, 'running'),
#     )
#
#     trade_state_choices = (
#         (TradeState.WAITING.value, TradeState.WAITING.name),
#         (TradeState.ENTERED.value, TradeState.ENTERED.name),
#         (TradeState.ENTERING.value, TradeState.ENTERING.name),
#         (TradeState.EXITING.value, TradeState.EXITING.name),
#         (TradeState.FINISHED.value, TradeState.FINISHED.name),
#         (TradeState.CANCELING.value, TradeState.CANCELING.name),
#         (TradeState.CANCELED.value, TradeState.CANCELED.name),
#         (TradeState.IDLE.value, TradeState.IDLE.name),
#     )
#
#     order_types = (
#         (10, "NONE"),
#         (OrderType.MARKET.value, OrderType.MARKET.name),
#         (OrderType.STOP_MARKET.value, OrderType.STOP_MARKET.name),
#         (OrderType.LIMIT.value, OrderType.LIMIT.name),
#         (OrderType.VIRTUAL_STOP_Market.value, OrderType.VIRTUAL_STOP_Market.name),
#         (OrderType.VIRTUAL_STOP_LIMIT.value, OrderType.VIRTUAL_STOP_LIMIT.name),
#         (OrderType.STOP_LIMIT.value, OrderType.STOP_LIMIT.name),
#     )
#
#
# class Currency(models.Model):
#     class Meta:
#         verbose_name_plural = "Currencies"
#
#     name = models.CharField(max_length=255, unique=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def save(self, *args, **kwargs):
#         self.name = self.name.upper()
#         super(Currency, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return str(self.name)
#
#
# class Market(models.Model):
#     name = models.CharField(max_length=255)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def get_bot_token(self):
#         if self.is_binance():
#             return spot_bot_token
#         elif self.is_binance_future():
#             return future_bot_token
#         else:
#             return bot_token
#
#     def get_bot_address(self):
#         if self.is_binance():
#             return bot_address
#         elif self.is_binance_future():
#             return bot_address_future
#         else:
#             return bot_address
#
#     # MODIFY
#     def get_slug_name(self):
#         return self.name
#
#     @staticmethod
#     def binanace_state_to_order_state(state, order):
#         state = state.lower()
#         if state.__eq__("ack") or state.__eq__("partialfill") or state.__eq__("new") or state.__eq__(
#                 "partially_filled"):
#             return OrderState.RUNNING.value
#         if state.__eq__("canceled"):
#             return OrderState.CANCELED.value
#         if state.__eq__("fullyfill") or state.__eq__("filled"):
#             return OrderState.FINISHED.value
#         if state.__eq__("expired"):
#             return OrderState.EXPIRED.value
#         # Expired, IocNoFill, FailedBlocking, FailedMatching, Unknown
#         # MODIFY : maybe later. don't change state if it was unknown for now...
#         # log.error(f"state ({state} is none of the recognizable states of Binance order")
#         raise Exception(f"{order} state ({state} is none of the recognizable states of Binance order")
#
#     @staticmethod
#     def bitmex_state_to_order_state(state):
#         # RUNNING = "New"
#         # FINISHED = "Filled"
#         # CANCELED = "Canceled"
#         # REJECTED = "Rejected"
#         state = state.lower()
#         if state.__eq__("new") or state.__eq__("partiallyfilled"):
#             return OrderState.RUNNING.value
#         if state.__eq__("canceled") or state.__eq__("rejected"):
#             return OrderState.CANCELED.value
#         if state.__eq__("filled"):
#             return OrderState.FINISHED.value
#         # Expired, IocNoFill, FailedBlocking, FailedMatching, Unknown
#         # MODIFY : maybe later. don't change state if it was unknown for now...
#         raise Exception(f"state ({state} is none of the recognizable states of Bitmex order")
#
#     def is_bitmex(self):
#         return self.name.lower().__eq__("bitmex")
#
#     def is_binance(self):
#         return self.name.lower().__eq__("binance")
#
#     def is_binance_future(self):
#         return self.name.lower().__eq__("binance_future")
#
#     def __str__(self):
#         return self.name
#
#
# redis = Redis()
#
#
# class Symbol(models.Model):
#     first = models.ForeignKey(Currency, related_name='first', on_delete=models.CASCADE, null=True, blank=True)
#     second = models.ForeignKey(Currency, related_name='second', on_delete=models.CASCADE, null=True,
#                                blank=True)
#     string = models.CharField(max_length=31, null=True, blank=True)
#     market = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True, blank=True)
#     active = models.BooleanField(default=True)
#     price_precision = models.DecimalField(max_digits=16, decimal_places=8, default=1)
#     quantity_precision = models.DecimalField(max_digits=16, decimal_places=8, default=1)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     trajectory = models.TextField(null=True, blank=True)
#     last_price_buy = models.DecimalField(max_digits=16, decimal_places=8, default=0)
#     last_price_sell = models.DecimalField(max_digits=16, decimal_places=8, default=0)
#     high = models.DecimalField(max_digits=16, decimal_places=8, default=0)
#     low = models.DecimalField(max_digits=16, decimal_places=8, default=1000000)
#     bin_update = models.DateTimeField(null=True, blank=True)
#     last_update = models.DateTimeField(auto_now=True)
#
#     # Binanace specific
#     # amount_step_size = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
#     # price_step_size = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
#     minimum_order_quote_size = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
#     minimum_quantity = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
#     price_sensitivity = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
#
#     class Meta:
#         unique_together = ('first', 'second', 'market')
#
#     def set_high_low(self, high, low, only_cache=False):
#         if settings.HAS_REDIS:
#             redis.set_symbol_high_low(self, high, low)
#             if only_cache:
#                 return
#         with transaction.atomic():  # this is to lock symbol
#             symbol = Symbol.objects.filter(pk=self.pk).select_for_update().get()
#             if are_equal(high, self.high) and are_equal(low, self.low):
#                 symbol.bin_update = datetime.now()
#                 symbol.save()
#                 return
#             symbol.add_trajectory_message(f"High {high},\tLow {low}")
#             symbol.high = str(high)
#             symbol.low = str(low)
#             symbol.bin_update = datetime.now()
#             symbol.save()
#
#     def set_last_price(self, price_buy, price_sell, only_cache=False):
#         if settings.HAS_REDIS:
#             redis.set_symbol_ask_bid(self, ask=price_sell, bid=price_buy)
#             if only_cache:
#                 return
#
#         with transaction.atomic():  # this is to lock symbol
#             symbol = Symbol.objects.filter(pk=self.pk).select_for_update().get()
#             if are_equal(price_buy, symbol.last_price_buy):
#                 # this updates the last_update for symbol
#                 symbol.save()
#                 # didn't change DB price
#                 return False
#             symbol.add_trajectory_message(f"ask {price_sell},\t bid {price_buy}")
#             symbol.last_price_buy = str(price_buy)
#             symbol.last_price_sell = str(price_sell)
#             symbol.save()
#             # changed DB price
#             return True
#
#     def _get_max_price_progress(self, is_exit, is_long):
#         price = self.father_get_price(is_exit=not is_exit, is_long=is_long, max_price_progress=False)
#         cached_high, cached_low = redis.get_symbol_high_low(symbol=self)
#
#         if cached_high is not None:
#             if is_long:
#                 return max(price, cached_high)
#             else:
#                 return min(price, cached_low)
#
#         if self.is_updating(check_bin=True):
#             if is_long:
#                 return max(price, self.high)
#             else:
#                 return min(price, self.low)
#         log.warning(f"Bins {self.market}:{self} are not updated... returning father_get_price as high")
#         return price
#
#     def get_quantity_from_quote_at_stake(self, quote_at_stake, price=None):
#         if self.market.is_bitmex():
#             return self.normalize_quantity(quote_at_stake)
#         elif self.market.is_binance() or self.market.is_binance_future():
#             if price is None:
#                 price = self.father_get_price(False, False)
#             price = Decimal(price)
#             return self.normalize_quantity(quote_at_stake / price, price=price)
#         else:
#             raise ValueError("Market is not recognized")
#
#     def get_quote_from_quantity(self, quantity, price=None):
#         if self.market.is_bitmex():
#             return quantity
#         elif self.market.is_binance() or self.market.is_binance_future():
#             if price is None:
#                 price = self.father_get_price(False, False)
#             price = Decimal(price)
#             return quantity * price
#         else:
#             raise ValueError("Market is not recognized")
#
#     @staticmethod
#     def update_binance_future_symbols():
#         r = requests.get('https://www.binance.com/fapi/v1/exchangeInfo')
#         print(r)
#         if r.status_code != 200:
#             return False
#         response = r.json()
#         symbols = response.get('symbols')
#         log.debug(f"Got {len(symbols)} symbols from Binance Future API call.")
#         # local_symbols = Symbol.objects.filter(market__name="Binanace")
#         for symbol in symbols:
#             try:
#                 local_symbol = Symbol.objects.get(first__name=symbol.get('baseAsset'),
#                                                   second__name=symbol.get('quoteAsset'),
#                                                   market__name__iexact="Binance_Future")
#                 filters = symbol.get('filters')
#                 local_symbol.price_precision = filters[0].get('tickSize')
#                 local_symbol.quantity_precision = filters[2].get('stepSize')
#                 local_symbol.minimum_quantity = filters[2].get('minQty')
#                 local_symbol.save()
#                 log.debug(f"Successfully updated {local_symbol}")
#             except Symbol.MultipleObjectsReturned:
#                 log.error(
#                     Symbol.objects.filter(first__name=symbol.get('baseAsset'), second__name=symbol.get('quoteAsset')))
#             except Symbol.DoesNotExist:
#                 pass
#
#     @staticmethod
#     def update_binance_symbols():
#         r = requests.get('https://api.binance.com/api/v1/exchangeInfo')
#         if r.status_code != 200:
#             return False
#         response = r.json()
#         symbols = response.get('symbols')
#         log.debug(f"Got {len(symbols)} symbols from Binance API call.")
#         # local_symbols = Symbol.objects.filter(market__name="Binanace")
#         for symbol in symbols:
#             try:
#                 local_symbol = Symbol.objects.get(first__name=symbol.get('baseAsset'),
#                                                   second__name=symbol.get('quoteAsset'),
#                                                   market__name__iexact="Binance")
#                 filters = symbol.get('filters')
#                 local_symbol.price_precision = filters[0].get('tickSize')
#                 local_symbol.quantity_precision = filters[2].get('stepSize')
#                 local_symbol.minimum_order_quote_size = filters[3].get('minNotional')
#                 local_symbol.save()
#                 log.debug(f"Successfully updated {local_symbol}")
#             except Symbol.MultipleObjectsReturned:
#                 log.error(
#                     Symbol.objects.filter(first__name=symbol.get('baseAsset'), second__name=symbol.get('quoteAsset')))
#             except Symbol.DoesNotExist:
#                 pass
#
#     def normalize_quantity(self, quantity, price=None):
#         quantity = Decimal(quantity)
#         # return "{:0.0{}f}".format(quantity, 4)
#         # quantity = round(quantity / self.quantity_precision, 0) * self.quantity_precision
#         # quantity = round(quantity / self.quantity_precision, 2) // 1 * self.quantity_precision
#         new_q = quantity // self.quantity_precision * self.quantity_precision
#         # if not are_equal(quantity, new_q):
#         #     log.debug_daily(f"normalize {quantity} on precision {self.quantity_precision} = {new_q}")
#         quantity = new_q
#         if self.market.is_binance_future():
#             if quantity < self.minimum_quantity:
#                 log.debug(f"quantity({float(quantity)} {self}) <"
#                           f" minimum_quantity({self.minimum_quantity})")
#                 # MODIFY: maybe it will be a bad idea
#                 # returns 0 if quantity provided in the price will lead to less than minimum_order_quote_size
#                 return 0
#             return quantity
#         else:
#             if price is None:
#                 price = self.father_get_price(False, False)
#             price = Decimal(price)
#             quote_at_stake = self.get_quote_from_quantity(quantity=quantity, price=price)
#             if quote_at_stake < self.minimum_order_quote_size:
#                 log.debug(f"quantity({float(quantity)} {self.string}) = quote at stake ({float(quote_at_stake)}) <"
#                           f" minimum_order_quote_size({self.minimum_order_quote_size})")
#                 # MODIFY: maybe it will be a bad idea
#                 # returns 0 if quantity provided in the price will lead to less than minimum_order_quote_size
#                 return 0
#             return quantity
#
#     def normalize_price(self, price, skip_is_normal=False):
#         if not skip_is_normal and self.price_is_normal(price=price, from_normalize=True):
#             return price
#         rounder = float(self.price_precision)
#         price_f = float(price)
#
#         return round(round(price_f / rounder, 0) * rounder, 8)
#
#     def price_is_normal(self, price, from_normalize=False):
#         price = float(price)
#         # print(f"price is normal on {price}")
#         current_price = float(self.father_get_price(False, True))
#         if not Decimal(1 - MIN_PRICE_DEVIATION / 100) < price / current_price < Decimal(1 + MAX_PRICE_DEVIATION / 100):
#             raise ValidationError(
#                 f"Price({float(price)}) can not be less than {MIN_PRICE_DEVIATION}% "
#                 f"or more than {MAX_PRICE_DEVIATION}% "
#                 f"of the current price({float(current_price)})")
#         if not are_equal(price % float(self.price_precision)):
#             if from_normalize:
#                 # print(f"{price} False")
#                 return False
#             else:
#                 raise ValidationError(f"Price must be a multiplier of {self.price_precision}")
#         else:
#             # print(f"{price} True")
#             return True
#
#     def quantity_is_normal(self, quantity, price=None, hypothetical=False):
#         if quantity % self.quantity_precision != 0:
#             raise ValidationError(f"Quantity must be a multiplier of {self.quantity_precision}")
#         if self.market.is_binance_future():
#             if quantity < self.minimum_quantity:
#                 raise ValidationError(f"Order quantity({float(quantity)} <"
#                                       f" minimum_quantity ({float(self.minimum_quantity)})")
#             return True
#         if hypothetical:
#             practical_min_notional = round(self.minimum_order_quote_size * Decimal(PRACTICAL_MIN_NOTIONAL_INDEX), 8)
#         else:
#             practical_min_notional = self.minimum_order_quote_size
#
#         quote = self.get_quote_from_quantity(quantity=quantity, price=price)
#         if quote < practical_min_notional:
#             raise ValidationError(f"Order value({float(quote)} {self.second}) <"
#                                   f" minimum order value ({float(practical_min_notional)} {self.second})"
#                                   f" with price ({float(price)})")
#         return True
#
#     def print_symbol(self, msg):
#         print(f"============ {self.market.name}:{self.string} {msg}")
#
#     def father_get_price_with_report(self, is_exit, is_long, max_price_progress=False):
#         if max_price_progress:
#             max_price_progress = self._get_max_price_progress(is_exit=is_exit, is_long=is_long)
#             self.print_symbol(f"max price {max_price_progress}")
#             return float(max_price_progress)
#
#         cached_price = self._get_cached_price(is_exit=is_exit, is_long=is_long)
#         if cached_price:
#             self.print_symbol(f"_get_cached_price {cached_price}")
#             return float(cached_price)
#
#         price = self._get_db_price(is_exit=is_exit, is_long=is_long)
#         if price:
#             self.print_symbol(f"_get_db_price {price}")
#             return float(price)
#         api_price = self._get_api_price(is_exit=is_exit, is_long=is_long)
#         self.print_symbol(f"_get_api_price {api_price}")
#         return float(api_price)
#
#     # NOTE: trade and signal set_last_price does not happen here
#     def father_get_price(self, is_exit, is_long, max_price_progress=False):
#         if max_price_progress:
#             return float(self._get_max_price_progress(is_exit=is_exit, is_long=is_long))
#
#         cached_price = self._get_cached_price(is_exit=is_exit, is_long=is_long)
#         if cached_price:
#             return float(cached_price)
#
#         price = self._get_db_price(is_exit=is_exit, is_long=is_long)
#         if price:
#             return float(price)
#         api_price = self._get_api_price(is_exit=is_exit, is_long=is_long)
#         return float(api_price)
#
#     def _get_cached_price(self, is_exit, is_long):
#         ask, bid = redis.get_symbol_ask_bid(self)
#         if ask is None:
#             return False
#         if (is_long and is_exit) or (not is_long and not is_exit):
#             # log.info(f"return cached price bid: {bid} for {self}. exit={is_exit}, long={is_long}")
#             return bid
#         # log.info(f"return cached price ask: {ask} for {self}. exit={is_exit}, long={is_long}")
#         return ask
#
#     def _get_db_price(self, is_exit, is_long):
#         if not self.is_updating():
#             return False
#         if self.last_price_buy is None or self.last_price_sell is None:
#             return False
#         if (is_long and is_exit) or (not is_long and not is_exit):
#             return self.last_price_buy
#         return self.last_price_sell
#
#     def _get_api_price(self, is_exit, is_long):
#         log.warning("Unfortunately [No DB] get_price through rest-API for %s" % self, add_to_file=False)
#         try:
#             if self.market.is_bitmex():
#                 response = Bitmex.get_price(symbol=self.string)
#                 if len(response) < 1:
#                     raise Exception("Symbol not found")
#                 price_buy = response[1]['price']
#                 price_sell = response[0]['price']
#                 # MODIFY: maybe it's not a good idea to update it with API (sets last update)
#                 changed = self.set_last_price(price_buy=price_buy, price_sell=price_sell)
#                 if changed:
#                     log.warning(f"======== API call changed DB price for Bitmex:{self}", add_to_file=True,
#                                 notify_bot=True)
#                 if (not is_long and not is_exit) or (
#                         is_long and is_exit):
#                     # side[1] = buy , side [0] = sell
#                     return price_buy
#                 else:
#                     return price_sell
#             elif self.market.is_binance():
#                 market_object = Binance(
#                     # MODIFY CRITICAL: this uses Hassan's API key and secred
#                     public_key=settings.bi_key,
#                     private_key=settings.bi_sec,
#                 )
#                 price = market_object.get_price(symbol=self.string)
#                 # MODIFY: separate sell and buy side
#                 # MODIFY: maybe it's not a good idea to update it with API (sets last update)
#                 changed = self.set_last_price(price, price)
#                 if changed:
#                     # MODIFY: it doesnt notify bot anymore
#                     log.warning(f"======== API call changed DB price for Binance:{self}", add_to_file=False,
#                                 notify_bot=False)
#                 return price
#             elif self.market.is_binance_future():
#                 market_object = BinanceFuture(
#                     # MODIFY CRITICAL: this uses Hassan's API key and secred
#                     public_key=settings.bi_key,
#                     private_key=settings.bi_sec,
#                 )
#                 price = market_object.get_price(symbol=self.string)
#                 # MODIFY: separate sell and buy side
#                 # MODIFY: maybe it's not a good idea to update it with API (sets last update)
#                 changed = self.set_last_price(price, price)
#                 if changed:
#                     # MODIFY: it doesnt notify bot anymore
#                     log.warning(f"======== API call changed DB price for Binance:{self}", add_to_file=False,
#                                 notify_bot=False)
#                 return price
#             else:
#                 raise Exception("market is not recognised")
#         except RetryException as e:
#             raise HandledException(e)
#
#     def is_updating(self, check_bin=False):
#         if check_bin:
#             t_delta = (datetime.now().replace(tzinfo=None) - self.bin_update.replace(tzinfo=None)).seconds
#             return t_delta < MAX_TIMEOUT_BIN_1_MIN
#         t_delta = (datetime.now().replace(tzinfo=None) - self.last_update.replace(tzinfo=None)).seconds
#         return t_delta < MAX_TIMEOUT_PRICE
#
#     # update_time
#     def update_time(self, bin=False):
#         with transaction.atomic():  # this is to lock symbol
#             symbol = Symbol.objects.filter(pk=self.pk).select_for_update().get()
#             if not bin:
#                 symbol.save()
#             else:
#                 symbol.bin_update = datetime.now()
#                 symbol.save()
#
#     def add_trajectory_message(self, msg, from_log=False):
#         too_big, text = summarize_log(self.trajectory)
#         if too_big:
#             log.info("Symbol[%d] trajectory was too big and summarized" % self.pk)
#             self.trajectory = text
#             self.save()
#
#         if not from_log:
#             msg = datetime.now().replace(microsecond=0).__str__() + ": " + msg
#         msg = msg + "\n"
#         if self.trajectory is None:
#             self.trajectory = ""
#         self.trajectory = msg + self.trajectory
#         self.save()
#
#     def __str__(self):
#         return f"{self.first}{self.second}"


# class SignalChannel(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     nick_name = models.CharField(max_length=255, unique=True, blank=False, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     creator_profile = models.ForeignKey("analyzer.Profile", on_delete=models.SET_NULL, null=True, blank=False,
#                                         related_name="channel_creator_profile")
#     # MODIFY delete user
#     # creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
#     description = models.TextField(blank=True)
#
#     @staticmethod
#     def get_or_create_channel_for_analyst(analyst):
#         try:
#             channel = SignalChannel.objects.get(creator_profile=analyst)
#         except SignalChannel.MultipleObjectsReturned:
#             SignalChannel.objects.filter(creator_profile=analyst).delete()
#             channel = SignalChannel.objects.create(
#                 creator_profile=analyst,
#                 name=analyst.__str__() + "_channel",
#                 nick_name=analyst.__str__() + "_channel",
#             )
#         except SignalChannel.DoesNotExist:
#             channel = SignalChannel.objects.create(
#                 creator_profile=analyst,
#                 name=analyst.__str__() + "_channel",
#                 nick_name=analyst.__str__() + "_channel",
#             )
#         return channel
#
#     def __str__(self):
#         return self.nick_name


class Signal(models.Model):
    # channel = models.ForeignKey(SignalChannel, on_delete=models.SET_NULL, null=True, blank=True)
    # MODIFY delete user
    # creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    creator_profile = models.ForeignKey("analyzer.Profile", on_delete=models.SET_NULL, null=True, blank=False)
    # market = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True, blank=False)
    valid = models.BooleanField(default=False)
    mini = models.BooleanField(default=False)
    deposit_share = models.DecimalField(max_digits=2, decimal_places=0, default=0)
    # position = models.PositiveSmallIntegerField(choices=Position.choices())
    # symbol = models.ForeignKey(Symbol, on_delete=models.SET_NULL, null=True, blank=False)
    entry_zone_low = models.DecimalField(max_digits=16, decimal_places=8)
    entry_zone_high = models.DecimalField(max_digits=16, decimal_places=8)
    targets = models.CharField(max_length=511)
    stop_loss = models.DecimalField(max_digits=16, decimal_places=8)
    cross_leverage = models.BooleanField(default=False)
    leverage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    trajectory = models.TextField(null=True, blank=True)
    last_price = models.DecimalField(max_digits=16, decimal_places=8, default=0)
    last_price_sell = models.DecimalField(max_digits=16, decimal_places=8, default=0)
    bot_message_id = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    should_have_socket = models.BooleanField(default=True)

    # def clean_entry_zone_low(self):
    #     self.entry_zone_low = self.symbol.normalize_price(self.entry_zone_low)

    # def clean(self):
    #     self.entry_zone_low = self.symbol.normalize_price(self.entry_zone_low)
    #     self.entry_zone_high = self.symbol.normalize_price(self.entry_zone_high)
    #     self.stop_loss = self.symbol.normalize_price(self.stop_loss)
    #
    #     if not self.mini:
    #         self.normalize_targets()
    #         targets = [self.symbol.normalize_price(target) for target in self.get_targets(already_normal=True)]
    #         self.targets = array_to_str(targets)
    #     self.are_targets_sorted()
    #
    #     if self.is_long() and not self.stop_loss < self.entry_zone_low < self.entry_zone_high:
    #         raise ValidationError("Invalid order of stop-loss, high and low for Long signal")
    #     if self.is_short() and not self.stop_loss > self.entry_zone_high > self.entry_zone_low:
    #         raise ValidationError("Invalid order of stop-loss, high and low for Short signal")
    #
    # def are_targets_sorted(self):
    #     if self.mini:
    #         return True
    #     targets = self.get_targets(already_normal=True)
    #     targets.insert(0, self.entry_zone_high)
    #     if self.is_long() and all(targets[i] <= targets[i + 1] for i in range(len(targets) - 1)):
    #         return True
    #     if self.is_short() and all(targets[i] >= targets[i + 1] for i in range(len(targets) - 1)):
    #         return True
    #     raise ValidationError("Signal targets and High are not in correct order")
    #
    # def invalidate_cancel_trades(self, user, comment):
    #     try:
    #         self.valid = False
    #         super().save()
    #         self.add_comment(f"Signal invalidated by {user} with message: '{comment}'", from_log=False)
    #         open_trades = Trade.objects.filter(signal=self, state__in=TradeState.get_active_states())
    #         self.add_comment(f"Initiating cancel process for open trades: {open_trades.all()}", from_log=False)
    #         for trade in open_trades:
    #             trade.queue_for_cancel(user=user,
    #                                    message=f"Trade canceled via signal cancellation with message: '{comment}'")
    #     except Exception as e:
    #         log.exception(e, traceback, user)
    #
    # def set_last_price(self, price_buy, price_sell):
    #     with transaction.atomic():  # this is to lock symbol
    #         signal = Signal.objects.filter(pk=self.pk).select_for_update().get()
    #         if are_equal(price_buy, signal.last_price):
    #             # updating last_update
    #             signal.save()
    #             return
    #         signal.add_trajectory_message("%s,\t %s" % (price_buy, price_sell))
    #         signal.last_price = str(price_buy)
    #         signal.last_price_sell = str(price_sell)
    #         signal.save()
    #
    # def add_comment(self, comment, from_log=False):
    #     if not from_log:
    #         comment = datetime.now().replace(microsecond=0).__str__() + ": " + comment
    #     comment = comment + "\n"
    #     if self.comment is None:
    #         self.comment = ""
    #     self.comment = comment + self.comment
    #     super().save()
    #     # self.save()
    #
    # def add_trajectory_message(self, msg, from_log=False):
    #     too_big, text = summarize_log(self.trajectory)
    #     if too_big:
    #         log.info("Signal[%d] trajectory was too big and summarized" % self.pk)
    #         self.trajectory = text
    #         self.save()
    #
    #     if not from_log:
    #         msg = datetime.now().replace(microsecond=0).__str__() + ": " + msg
    #     msg = msg + "\n"
    #     if self.trajectory is None:
    #         self.trajectory = ""
    #     self.trajectory = msg + self.trajectory
    #     self.save()
    #
    # def is_long(self):
    #     return self.position == Position.LONG.value
    #
    # def is_short(self):
    #     return self.position == Position.SHORT.value
    #
    # def is_in_entry_zone(self, price):
    #     return float(self.entry_zone_high) >= price >= float(self.entry_zone_low)
    #
    # def closer_side_of_entry_zone(self, price):
    #     # returns the closer side of entry zone
    #     price = float(price)
    #     if abs(price - float(self.entry_zone_high)) < abs(price - float(self.entry_zone_low)):
    #         return float(self.entry_zone_high)
    #     return float(self.entry_zone_low)
    #
    # def save(self, *args, **kwargs):
    #     self.clean()
    #     if self.pk:
    #         super(Signal, self).save(*args, **kwargs)
    #     else:
    #         super(Signal, self).save(*args, **kwargs)
    #         if self.valid:
    #             AutoTrade.create_trade_for_matching_auto_trades(self)
    #
    # def bot_user_str(self):
    #     return self.full_str()
    #
    # def full_str(self):
    #     mini = ""
    #     targets = ""
    #     validity = "Invalid"
    #
    #     if self.mini:
    #         mini = "(Mini)"
    #     else:
    #         targets = ",\nTargets: " + self.targets
    #
    #     if self.valid:
    #         validity = "Valid"
    #     return f"{self}\n({validity}){mini}\nSL: {self.stop_loss}\nLow: {self.entry_zone_low}\n" \
    #            f"High:{self.entry_zone_high}{targets}"
    #
    # def __str__(self):
    #     return f"Signal[{self.pk}]({self.market})({Position.get_string(self.position)})({self.symbol})" \
    #            f"(via {self.channel})"
    #
    # def normalize_targets(self):
    #     self.targets = array_to_str(str_to_float_array(self.targets, already_normal=False))
    #
    # def get_targets(self, already_normal=True):
    #     # MODIFY CRITICAL
    #     return str_to_float_array(self.targets, already_normal=already_normal)


# class Strategy(models.Model):
#     class Meta:
#         verbose_name_plural = "Strategies"
#
#     name = models.CharField(max_length=255, null=True, blank=True)
#     # creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
#     creator_profile = models.ForeignKey("accounts.Profile", on_delete=models.SET_NULL, null=True, blank=False,
#                                         related_name="strategy_creator_profile")
#     market = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True, blank=False)
#     valid = models.BooleanField(default=False)
#     comment = models.CharField(max_length=511, null=True, blank=True)
#     parameters = models.TextField(
#         null=True, blank=True,
#         default="{\"starting_coefficient\": 0.7,\"finishing_coefficient\": 0.3,\"zone_bias\": 1,\"limit_to_stop_index\": 0.8,\"max_profit\": 0.04, \"take_profit_array\": \"1\"}")
#     timestamp = models.DateTimeField(auto_now_add=True)
#     type = models.PositiveSmallIntegerField(choices=Choices.trade_strategy_type)
#
#     def __str__(self):
#         if self.name is not None:
#             return self.name
#         return f"strategy[{self.pk}]"
#
#     def get_take_profit_array(self):
#         try:
#             params = json.loads(self.parameters)
#             return str_to_float_array(params['take_profit_array'])
#         except KeyError:
#             raise Exception(f"Unable to extract take_profit_array from {self}")
#
#
# class Trade(models.Model):
#     # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
#     profile = models.ForeignKey("accounts.Profile", on_delete=models.SET_NULL, null=True, blank=False)
#     signal = models.ForeignKey(Signal, on_delete=models.SET_NULL, null=True, blank=False)
#     test = models.BooleanField(default=False)
#     strategy = models.ForeignKey(Strategy, on_delete=models.SET_NULL, null=True, blank=False)
#     quantity = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
#     # trail_percentage = models.DecimalField(max_digits=8, decimal_places=4, default=.5)
#     liquidation_price = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
#     state = models.PositiveSmallIntegerField(choices=Choices.trade_state_choices, default=1)
#     profit = models.FloatField(null=True, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     comment = models.TextField(null=True, blank=True, default="")
#     error = models.TextField(null=True, blank=True, default="")
#     last_price = models.DecimalField(max_digits=16, decimal_places=8, default=0)
#     last_progress_price = models.DecimalField(max_digits=16, decimal_places=8, default=0)
#     last_update = models.DateTimeField(auto_now=True)
#     trajectory = models.TextField(null=True, blank=True, default="")
#     auto_trade = models.ForeignKey('exchange.AutoTrade', on_delete=models.SET_NULL, null=True, blank=True)
#
#     @staticmethod
#     def get_unfinished_trades():
#         return Trade.objects.exclude(
#             state__in=[TradeState.FINISHED.value, TradeState.CANCELED.value, TradeState.IDLE.value])
#
#     def oms_side(self, exit):
#         if not exit:
#             return Side.Buy.value if self.signal.is_long() else Side.Sell.value
#         return Side.Sell.value if self.signal.is_long() else Side.Buy.value
#
#     class Meta:
#         indexes = [
#             models.Index(fields=['state'])
#         ]
#
#     @staticmethod
#     @background(schedule=1)
#     def warn_idle_state(trade_id, msg):
#         from telegram_bot.utils import BotNotification
#         # trade = Trade.objects.filter(pk=trade_id).select_for_update().get()
#         BotNotification.transmit_error(f"{msg}\nAttend to it immediately.")
#
#     def set_idle(self, msg):
#         with transaction.atomic():
#             trade = Trade.objects.filter(pk=self.pk).select_for_update().get()
#             msg = log.info(f"{trade.mini_str()} is set to IDLE state from {TradeState.get_string(trade.state)} "
#                            f"with message:\n{msg}", add_to_file=True)
#             trade.add_comment(msg, from_log=True)
#             trade.state = TradeState.IDLE.value
#             trade.save()
#             self.warn_idle_state(self.id, msg)
#
#     def clean(self):
#
#         # MODIFY: this does not get executed
#         # check in validators
#         # self.quantity is normal
#         self.quantity = self.signal.symbol.normalize_quantity(self.quantity, price=self.signal.entry_zone_high)
#         # self.quantity = self.signal.symbol.normalize_quantity(self.quantity, self.get_entry_price())
#         # MODIFY LATER
#         self.signal.symbol.quantity_is_normal(self.quantity, Decimal(self.signal.stop_loss), hypothetical=False)
#         # take_profit_array = str_to_float_array(
#         #     json.loads(self.strategy.parameters)['stop_parameters']["take_profit_array"])
#         # q_array = self.get_target_quantity_array(take_profit_array=take_profit_array)
#         # print(f"q_array: {q_array}\nsum: {sum(q_array)}\nquantity: {self.quantity}")
#         # if sum(q_array) != self.quantity:
#         #     raise ValidationError("total values don't match")
#
#     def get_target_quantity_array(self, quantity, take_profit_array):
#         quantity = self.signal.symbol.normalize_quantity(quantity=quantity, price=self.signal.stop_loss)
#         targets = self.signal.get_targets()
#         if len(take_profit_array) > len(targets):
#             take_profit_array = take_profit_array[0:len(targets)]
#         target_quantity_array = []
#         for i in range(len(take_profit_array)):
#             q = self.signal.symbol.normalize_quantity(
#                 quantity=quantity * Decimal(take_profit_array[i]),
#                 price=self.signal.stop_loss)
#             target_quantity_array.append(Decimal(q))
#
#         # print(type(self.quantity))
#         # print(type(target_quantity_array[0][1]))
#         remainder = quantity - sum(target_quantity_array)
#         print("before quantity:", quantity, " ", target_quantity_array, " remainder: ", remainder)
#         for i in range(target_quantity_array.__len__()):
#             if not are_equal(target_quantity_array[i]):
#                 target_quantity_array[i] += remainder
#                 break
#         if are_equal(sum(target_quantity_array)):
#             target_quantity_array[0] = remainder
#         print("after ", self.quantity, " array: ", target_quantity_array)
#
#         self.add_comment(f"target_quantity_array = {target_quantity_array}")
#         return target_quantity_array
#
#     def critical_error(self, msg):
#         try:
#             self.set_idle(msg)
#         except Exception as e:
#             log.exception(e, traceback, notify_bot=False)
#
#     def remainder(self):
#         return self.filled_enter_quantity() - self.filled_exit_quantity()
#
#     def filled_enter_quantity(self):
#         q = 0
#         for order in self.order_set.filter(is_exit=False):
#             q += order.filled_quantity - order.commission_from_asset
#         for order in self.oms_order_set.filter(is_exit=False):
#             q += order.filled_quantity
#         return q
#
#     def filled_exit_quantity(self):
#         q = 0
#         for order in self.order_set.filter(is_exit=True):
#             if order.filled_quantity is not None:
#                 q += order.filled_quantity
#         for order in self.oms_order_set.filter(is_exit=True):
#             if order.filled_quantity is not None:
#                 q += order.filled_quantity
#         # print("filled exit: ", q)
#         return q
#
#     def get_entry_price(self):
#         try:
#             entry_order = self.order_set.get(state=OrderState.FINISHED.value, is_exit=False)
#             if entry_order is not None and entry_order.fill_price is not None:
#                 return entry_order.fill_price
#             log.warning("'get_entry_price returned theoretical enter value for %s" % self)
#             return (self.signal.entry_zone_high + self.signal.entry_zone_low) / 2
#
#         except Order.DoesNotExist:
#             msg = log.error("Calling 'get_entry_price for %s raised Order.DoesNotExist exception. "
#                             "No FINISHED enter-order found in trade" % self)
#             self.add_error(msg)
#             log.warning("'get_entry_price' returned theoretical enter value for %s" % self)
#             return (self.signal.entry_zone_high + self.signal.entry_zone_low) / 2
#
#         except Exception as e:
#             msg = log.exception(e, traceback)
#             log.warning("'get_entry_price' returned theoretical enter value for %s" % self)
#             return (self.signal.entry_zone_high + self.signal.entry_zone_low) / 2
#
#     def set_last_price(self, price, msg="", progress_price=False):
#         if progress_price:
#             if are_equal(price, self.last_progress_price):
#                 return
#             self.add_trajectory_message(f"{price}\t{msg}", from_log=False)
#             # MODIFY: WTF! What the fuck is this Shit?
#             # full_clean on decimal_field gave exception
#             # [EXCEPTION][user = 9169093271] {'last_price': ['Ensure that there are no more than 8 decimal places.']}
#             # amount = decimal.Decimal(str(price))
#             self.last_progress_price = str(price)
#             self.save()
#         else:
#             if are_equal(price, self.last_price):
#                 return
#             self.add_trajectory_message(f"{price}\t\t{msg}", from_log=False)
#             # MODIFY: WTF! What the fuck is this Shit?
#             # full_clean on decimal_field gave exception
#             # [EXCEPTION][user = 9169093271] {'last_price': ['Ensure that there are no more than 8 decimal places.']}
#             # amount = decimal.Decimal(str(price))
#             self.last_price = str(price)
#             self.save()
#
#     @staticmethod
#     @background(schedule=1)
#     def notify_user_of_double_stops(trade_id):
#         try:
#             trade = Trade.objects.get(pk=trade_id)
#             email_api.double_stops(trade=trade)
#         except Exception as e:
#             log.exception(e, traceback)
#
#     @staticmethod
#     @background(schedule=1)
#     def notify_user_of_trade(trade_id):
#         try:
#             trade = Trade.objects.get(pk=trade_id)
#             email_api.enter_trade(trade=trade)
#             sms.enter_trade(trade=trade)
#             BotNotification(token=trade.signal.market.get_bot_token()).enter_trade(trade)
#         except Exception as e:
#             log.exception(e, traceback)
#
#     def save(self, *args, **kwargs):
#         self.clean()
#         if self.pk:
#             super(Trade, self).save(*args, **kwargs)
#             return
#         active_trades = Trade.objects.filter(
#             state__in=TradeState.get_active_states(),
#             profile=self.profile,
#             signal__market=self.signal.market,
#             signal__symbol=self.signal.symbol,
#         )
#         if active_trades.count() >= MAX_ACTIVE_TRADES_ON_SYMBOL:
#             # MODIFY: WHAT THE FUCK IS GOING ON?!
#             # it doens't make a process so I have to send the email synchronously
#             email_api.too_many_trades(self.profile.pk)
#             raise ValidationError(
#                 "User can't have more than %d active trades on the same symbol" % MAX_ACTIVE_TRADES_ON_SYMBOL)
#         # self.clean()
#         super(Trade, self).save(*args, **kwargs)
#         self.notify_user_of_trade(self.pk)
#
#     def close_remainder_position(self):
#         remainder = self.remainder()
#         self.add_comment(log.info(f"{self.mini_str()} remainder: {remainder}"), from_log=True)
#
#         remainder_quantity = self.signal.symbol.normalize_quantity(quantity=abs(remainder))
#         if are_equal(remainder_quantity):
#             self.add_comment("close_remainder_position successful (no remainder)")
#         else:
#             self.add_comment(log.info(f"Exiting Trade[{self.pk}] real remainder({float(remainder_quantity)})"), from_log=True)
#             if remainder < 0:
#                 is_exit = False
#             else:
#                 is_exit = True
#             try:
#                 from oms.models import Order as OMSOrder
#                 OMSOrder.ex_create_market_order(
#                     trade=self,
#                     symbol=self.signal.symbol,
#                     amount=remainder_quantity,
#                     side=self.oms_side(exit=is_exit),
#                     is_exit=is_exit
#                 )
#             except RetryException as e:
#                 self.add_error(log.info(f"Exiting remainder failed {e}"), from_log=True)
#                 raise HandledException(e.__str__())
#             except SynchronizeException as e:
#                 self.add_error(log.info(f"Exiting remainder failed {e}"), from_log=True)
#                 raise HandledException(e)
#             except AbortException as e:
#                 self.critical_error(log.info(f"Exiting remainder failed {e}"))
#                 raise HandledException(e.__str__())
#             except Exception as e:
#                 log.exception(e, traceback, user=self)
#                 self.critical_error(log.info(f"Exiting remainder failed {e}"))
#                 raise HandledException(e.__str__())
#             # from api import api_interface
#             # success = api_interface.market_order(self, quantity=remainder_quantity, is_exit=is_exit,
#             #                                      commission_protected=False)
#             self.add_comment("close_remainder_position successful")
#
#     def close_trade(self, final_state=TradeState.FINISHED.value, msg=None):
#         if msg is not None:
#             self.add_comment(msg)
#
#         # MODIFY CRITICAL NEW : check if all orders are FINISHED
#         self.close_remainder_position()
#
#         self.add_comment("trade was completed because all orders are filled")
#         self.state = final_state
#         self.save()
#         self.calculate_profit_and_handle_exceptions()
#
#     def get_closest_limit(self, price=None, is_exit=False):
#         # if price is none get market price
#         if price is None:
#             from api import api_interface
#             price = api_interface.get_price(self, is_exit=is_exit)
#         round_value = float(self.signal.symbol.price_precision)
#         if self.signal.position == Position.LONG.value and not is_exit:
#             # utils.info("relevant price: %s. return -%s" % (price, round_value))
#             return price - round_value
#         if self.signal.position == Position.SHORT.value and is_exit:
#             # utils.info("relevant price: %s. return -%s" % (price, round_value))
#             return price - round_value
#         # utils.info("relevant price: %s. return +%s" % (price, round_value))
#         return price + round_value
#
#     # new_stop = models.DecimalField(max_digits=16, decimal_places=8, null=True)
#     def calculate_profit_and_handle_exceptions(self):
#         try:
#             self.calculate_profit()
#         except ZeroDivisionError as e:
#             self.add_error(e.__str__())
#         except Exception as e:
#             error_message = log.exception(e, traceback, self.profile)
#             self.add_error(error_message, from_log=True)
#
#     def calculate_profit(self):
#         if self.state != TradeState.FINISHED.value and self.state != TradeState.CANCELED.value:
#             return
#         for order in self.order_set.all():
#             # for completing the fill_price params
#             order.is_in_active_state(force_api_call=True)
#         profit_percentage = 0
#         enter_value = 0
#         exit_value = 0
#         enter_orders = []
#         exit_orders = []
#         symbol = self.signal.symbol
#         if self.is_bitmex():
#             from api import api_interface
#             market_object = api_interface.get_bitmex_market_object(self)
#             user_commission = market_object.get_user_commission()
#             user_commission = user_commission[str(symbol)]
#             user_commission_taker = user_commission['takerFee']
#             user_commission_maker = user_commission['makerFee']
#             if self.signal.leverage is None:
#                 leverage = float(100)
#             else:
#                 leverage = float(self.signal.leverage)
#
#             for order_ins in self.order_set.all():
#
#                 if order_ins.is_enter_order():
#                     enter_orders.append(order_ins)
#                 elif order_ins.is_exit_order():
#                     exit_orders.append(order_ins)
#
#             for order_ins in enter_orders:
#                 filled_price = float(order_ins.fill_price)
#                 quantity = float(order_ins.quantity)
#                 if order_ins.is_maker():
#                     if self.signal.position == Position.SHORT.value:
#                         enter_value += quantity / filled_price * (1 + user_commission_maker)
#                     elif self.signal.position == Position.LONG.value:
#                         enter_value += quantity / filled_price * (1 - user_commission_maker)
#                 else:
#                     if self.signal.position == Position.SHORT.value:
#                         enter_value += quantity / filled_price * (1 + user_commission_taker)
#                     elif self.signal.position == Position.LONG.value:
#                         enter_value += quantity / filled_price * (1 - user_commission_taker)
#
#             for order_ins in exit_orders:
#                 filled_price = float(order_ins.fill_price)
#                 quantity = float(order_ins.quantity)
#                 if order_ins.is_maker():
#                     if self.signal.position == Position.SHORT.value:
#                         exit_value += quantity / filled_price * (1 - user_commission_maker)
#                     elif self.signal.position == Position.LONG.value:
#                         exit_value += quantity / filled_price * (1 + user_commission_maker)
#                 else:
#                     if self.signal.position == Position.SHORT.value:
#                         exit_value += quantity / filled_price * (1 - user_commission_taker)
#                     elif self.signal.position == Position.LONG.value:
#                         exit_value += quantity / filled_price * (1 + user_commission_taker)
#             if self.signal.position == Position.SHORT.value:
#                 profit_quant = -enter_value + exit_value
#                 profit_percentage = profit_quant / enter_value * leverage
#             elif self.signal.position == Position.LONG.value:
#                 profit_quant = -exit_value + enter_value
#                 profit_percentage = profit_quant / enter_value * leverage
#
#         elif self.is_binance():
#             from api import api_interface
#             market_object = api_interface.get_binance_market_object(self)
#             user_commission = market_object.get_user_commission()
#             user_commission_taker = user_commission['takerCommission'] / 10000
#             user_commission_maker = user_commission['makerCommission'] / 10000
#             leverage = 1
#             for order_ins in self.order_set.all():
#                 if order_ins.is_enter_order():
#                     enter_orders.append(order_ins)
#                 elif order_ins.is_exit_order():
#                     exit_orders.append(order_ins)
#
#             for order_ins in enter_orders:
#                 filled_price = float(order_ins.fill_price)
#                 quantity = float(order_ins.quantity)
#                 if order_ins.is_maker():
#                     if self.signal.position == Position.SHORT.value:
#                         enter_value += (quantity * filled_price) * (1 - user_commission_maker)
#                     elif self.signal.position == Position.LONG.value:
#                         enter_value += (quantity * filled_price) * (1 + user_commission_maker)
#                 else:
#                     if self.signal.position == Position.SHORT.value:
#                         enter_value += (quantity * filled_price) * (1 - user_commission_taker)
#                     elif self.signal.position == Position.LONG.value:
#                         enter_value += (quantity * filled_price) * (1 + user_commission_taker)
#
#             for order_ins in exit_orders:
#                 filled_price = float(order_ins.fill_price)
#                 quantity = float(order_ins.quantity)
#                 if order_ins.is_maker():
#                     if self.signal.position == Position.SHORT.value:
#                         exit_value += (quantity * filled_price) * (1 + user_commission_maker)
#                     elif self.signal.position == Position.LONG.value:
#                         exit_value += (quantity * filled_price) * (1 - user_commission_maker)
#                 else:
#                     if self.signal.position == Position.SHORT.value:
#                         exit_value += (quantity * filled_price) * (1 + user_commission_taker)
#                     elif self.signal.position == Position.LONG.value:
#                         exit_value += (quantity * filled_price) * (1 - user_commission_taker)
#                 if self.signal.position == Position.SHORT.value:
#                     profit_quant = enter_value - exit_value
#                     profit_percentage = profit_quant / enter_value
#                 elif self.signal.position == Position.LONG.value:
#                     profit_quant = exit_value - enter_value
#                     profit_percentage = profit_quant / enter_value
#         else:
#             # AMIRREZA MODIFY
#             # ADD FUTURE CALCULATE PROFIT
#             raise Exception("market is not recognised")
#
#         # if self.signal.position == Position.SHORT.value:
#         #     profit_quant = -enter_value + exit_value
#         #     profit_percentage = float(profit_quant) / enter_value * leverage
#         # elif self.signal.position == Position.LONG.value:
#         #     profit_quant = -exit_value + enter_value
#         #     profit_percentage = float(profit_quant) / enter_value * leverage
#
#         profit_percentage = round(profit_percentage, 8)
#         self.profit = profit_percentage
#         self.save()
#
#     def add_trajectory_message(self, msg, from_log=False):
#         too_big, text = summarize_log(self.trajectory)
#         if too_big:
#             log.info("Trade[%d] trajectory was too big and summarized" % self.pk)
#             self.trajectory = text
#             self.save()
#
#         if not from_log:
#             msg = datetime.now().replace(microsecond=0).__str__() + ": " + msg
#         msg = msg + "\n"
#         if self.trajectory is None:
#             self.trajectory = ""
#         self.trajectory = msg + self.trajectory
#         super().save()
#
#     def add_comment(self, comment, from_log=False):
#         too_big, text = summarize_log(self.comment)
#         if too_big:
#             log.info("Trade[%d] comment was too big and summarized" % self.pk)
#             self.comment = text
#             self.save()
#
#         if not from_log:
#             comment = datetime.now().replace(microsecond=0).__str__() + ": " + comment
#         self.add_trajectory_message(comment, from_log=True)
#         comment = comment + "\n"
#         if self.comment is None:
#             self.comment = ""
#         self.comment = comment + self.comment
#         super().save()
#
#     def add_error(self, error_message, from_log=False):
#         too_big, text = summarize_log(self.error)
#         if too_big:
#             log.info("Trade[%d] error was too big and summarized" % self.pk)
#             self.error = text
#             self.save()
#
#         if not from_log:
#             error_message = datetime.now().replace(microsecond=0).__str__() + ": " + error_message
#         self.add_trajectory_message(error_message, from_log=True)
#         error_message = error_message + "\n"
#         if self.error is None:
#             self.error = ""
#         self.error = error_message + self.error
#         self.save()
#
#     def is_bitmex(self):
#         return self.signal.market.is_bitmex()
#
#     def is_binance(self):
#         return self.signal.market.is_binance()
#
#     def is_binance_future(self):
#         return self.signal.market.is_binance_future()
#
#     def mini_str(self):
#         return f"Trade[{self.pk}]({self.profile})(Signal[{self.signal_id}])"
#
#     def __str__(self):
#         return "Trade[%d](%s, %s)" % (self.pk, self.profile, self.signal)
#
#     def full_str(self):
#         return f"Trade[{self.pk}]({self.profile})\n{self.signal.full_str()}"
#
#     def bot_user_str(self):
#         return self.full_str()
#
#     class CancelingInProgress(Exception):
#         pass
#
#     def disable_account(self):
#         exchange_account = self.profile.exchangeaccount_set.get(market=self.signal.market)
#         exchange_account.enable = False
#         exchange_account.save()
#
#     def queue_for_cancel(self, user=None, message=None):
#         with transaction.atomic():
#             trade = Trade.objects.filter(pk=self.pk).select_for_update().get()
#             if user is None:
#                 user = "SYSTEM"
#             if message is not None:
#                 self.add_comment(f"Queued for cancel with message: '{message}'")
#             msg = log.info(f"user[{user}] tried to cancel the trade from state {TradeState.get_string(self.state)}",
#                            add_to_file=False)
#             self.add_comment(msg, from_log=True)
#
#             # FINISHED AND CANCELED trades are all the same
#             if self.state == TradeState.FINISHED.value or self.state == TradeState.CANCELED.value:
#                 msg = log.warning("Trade is already closed. Command aborted", add_to_file=False)
#                 self.add_comment(msg, from_log=True)
#                 return
#
#             # ASSUMPTION: there are no orders in a waiting trade (or just virtual orders?)
#             if self.state == TradeState.WAITING.value:
#                 self.state = TradeState.CANCELED.value
#                 self.save()
#                 msg = log.info("Trade was successfully CANCELED.")
#                 self.add_comment(msg, from_log=True)
#                 return
#
#             if trade.state == TradeState.ENTERED.value or trade.state == TradeState.ENTERING.value:
#                 trade.state = TradeState.CANCELING.value
#                 trade.save()
#
#     def cancel_oms_orders(self):
#         from oms.models import OrderState as OMSOrderState
#         for order in self.oms_order_set.filter(state=OMSOrderState.Active.value):
#             try:
#                 order.exe_cancel_order()
#             except (RetryException, SynchronizeException) as e:
#                 raise HandledException(e)
#             except AbortException as e:
#                 self.critical_error(e.__str__())
#                 raise HandledException(e)
#             except Exception as e:
#                 msg = log.exception(e, traceback, self.profile)
#                 self.critical_error(msg)
#                 raise HandledException(e)
#
#     def cancel_oco_orders(self):
#         for oco in self.oco_set.all():
#             oco.cancel_oco()
#
#     def cancel_exchange_orders(self):
#         for exchange_order in self.order_set.all():
#             exchange_order.cancel_order(cancel_order_from_twin=False, source="cancel_trade")
#
#     def cancel_all_orders(self):
#         self.cancel_oco_orders()
#         self.cancel_oms_orders()
#         self.cancel_exchange_orders()
#         self.add_comment(log.info(f"cancel_all_orders executed for {self.mini_str()}"), from_log=True)
#
#     def cancel_trade(self):
#         # trade = Trade.objects.filter(pk=self.pk).select_for_update().get()
#         if self.state != TradeState.CANCELING.value:
#             raise HandledException(f"{self.mini_str()} is not in the CANCELING state.")
#
#         self.add_comment(log.info(f"Initiating cancel process for {self.mini_str()}"), from_log=True)
#
#         self.cancel_all_orders()
#
#         self.close_trade(final_state=TradeState.CANCELED.value)
#
#         self.add_comment(log.info("%s was successfully CANCELED." % self), from_log=True)
#
#     def execute_trade(self):
#         from trade.urls import measure_time
#         before = measure_time("Trade.execute_trade()", depth=1)
#         if self.order_set.all().__len__() > MAX_ORDERS_PER_TRADE:
#             self.close_trade(msg=f"Trade canceled due to reaching MAX_ORDERS_PER_TRADE({MAX_ORDERS_PER_TRADE})")
#             return
#         before = measure_time("MAX_ORDERS_PER_TRADE time", start_time=before, depth=1)
#         if not self.signal.valid:
#             self.queue_for_cancel(message="Trade queued for cancel because signal is not valid anymore")
#             # return
#
#         if self.strategy.type == StrategyType.TRAIL_TARGETS_WITH_MARKET.value:
#             from exchange.strategy.market_targets import TrailTargetsWithMarket
#             TrailTargetsWithMarket.execute(self)
#         elif self.strategy.type == StrategyType.TRAIL_NO_TARGETS_WITH_LIMIT.value:
#             from exchange.strategy.limit_no_target import TrailNoTargetsWithLimit
#             TrailNoTargetsWithLimit.execute(self)
#         elif self.strategy.type == StrategyType.TRAIL_TARGETS_WITH_LIMIT.value:
#             from exchange.strategy.limit_targets import TrailTargetsWithLimit
#             TrailTargetsWithLimit.execute(self)
#         elif self.strategy.type == StrategyType.NO_TARGETS_WITH_MARKET.value:
#             from exchange.strategy.market_no_targets import TrailNoTargetsWithMarket
#             TrailNoTargetsWithMarket.execute(self)
#         elif self.strategy.type == StrategyType.TAKE_PROFIT_ON_TARGET.value:
#             from exchange.strategy.take_profit import TakeProfit
#             before = measure_time("import TakeProfit time", start_time=before, depth=1)
#             TakeProfit.execute(self)
#         elif self.strategy.type == StrategyType.TAKE_PROFIT_OCO.value:
#             from exchange.strategy.take_profit_main import TakeProfitOco
#             before = measure_time("import TakeProfitOco time", start_time=before, depth=1)
#             TakeProfitOco.execute(self)
#         elif self.strategy.type == StrategyType.PRICE_FOLLOWER.value:
#             from exchange.strategy.market_targets import S2
#             S2.execute(self)
#         elif self.strategy.type == StrategyType.MULTIPLE_TRAIL.value:
#             from exchange.strategy.market_targets import S3
#             S3.execute(self)
#         else:
#             raise ValueError(log.error("INVALID STRATEGY TYPE"))
#         before = measure_time("Trade.execute_trade() time", start_time=before, depth=1)
#
#
# class Order(models.Model):
#     trade = models.ForeignKey(Trade, on_delete=models.SET_NULL, null=True, blank=False)
#     market = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True, blank=True)
#     order_type = models.PositiveSmallIntegerField(choices=Choices.order_types, default=10)
#     oco_order = models.BooleanField(default=False)
#     twin = models.OneToOneField("exchange.Order", on_delete=models.SET_NULL, null=True, blank=True)
#     state = models.PositiveSmallIntegerField(choices=Choices.order_state_choices, default=OrderState.WAITING.value)
#     # old_type = models.PositiveSmallIntegerField(choices=Choices.old_order_type_choices, default=10)
#     quantity = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
#     filled_quantity = models.DecimalField(max_digits=16, decimal_places=8, default=0, blank=True, null=True)
#     commission_from_asset = models.DecimalField(max_digits=16, decimal_places=8, default=0, blank=True, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     stop_price = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
#     price = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
#     fill_price = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
#     error = models.TextField(null=True, blank=True)
#     comment = models.TextField(null=True, blank=True)
#     is_exit = models.BooleanField(default=False)
#     unique_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
#     last_update = models.DateTimeField(auto_now=True)
#
#     def is_asset_currency(self, currency_name):
#         return self.trade.signal.symbol.first.name == currency_name
#     #     state = OrderState.RUNNING.value,
#     #     order_type__in = OrderType.get_real_order_types(),
#     #     trade__isnull = False
#     #
#     # ).order_by('last_update')
#     #     class Meta:
#     #         indexes = [
#     #             models.Index(fields=['state', 'order_type', 'trade', 'last_update']),
#     #         ]
#
#     def update_binance_order_with_json(self, response, source):
#         filled_quantity = response['executedQty']
#         cumulative_quote_qty = response['cummulativeQuoteQty']
#         state = response['status']
#         price = float(response['price'])
#         # quantity = ?
#         # STOP picec = ?
#         state = Market.binanace_state_to_order_state(state, order=self)
#         # MODIFY: if Binance ever corrected spelling of 'cumulative'...
#         try:
#             fill_price = float(cumulative_quote_qty) / float(filled_quantity)
#         except ZeroDivisionError:
#             fill_price = None
#         commission_from_asset = 0
#         try:
#             for fill in response['fills']:
#                 if self.is_asset_currency(fill["commissionAsset"]):
#                     commission_from_asset += float(fill["commission"])
#         except KeyError:
#             commission_from_asset = None
#             # log.warning(f"KeyError at update_binance_order_with_json: {e}", notify_bot=True)
#         except Exception as e:
#             commission_from_asset = None
#             log.exception(e, traceback)
#
#         changed = self.update_order_params(
#             source=source, state=state, quantity=None, price=price, stop_price=None,
#             filled_quantity=filled_quantity, fill_price=fill_price, commission_from_asset=commission_from_asset)
#         return changed
#
#     def update_bitmex_order_with_json(self, response, source):
#         quantity = response["orderQty"]
#         price = response["price"]
#         stop_price = response["stopPx"]
#         state = response['ordStatus']
#         state = Market.bitmex_state_to_order_state(state)
#         filled_quantity = response["cumQty"]
#         fill_price = response["avgPx"]
#         text = response["text"]
#         changed = self.update_order_params(source=source, state=state, quantity=quantity, price=price,
#                                            stop_price=stop_price,
#                                            filled_quantity=filled_quantity, fill_price=fill_price)
#         self.add_comment(text)
#         return changed
#
#     def update_order_params(self, source, state=None, stop_price=None, price=None, fill_price=None,
#                             filled_quantity=None, quantity=None, commission_from_asset=None, twin=None,
#                             force_log=False):
#         with transaction.atomic():
#             # MODIFY VERIFY: should i use order or self is enough?
#             changed = False
#             order = Order.objects.filter(pk=self.pk).select_for_update().get()
#             str_msg = f"Update command (from {source}) on (Order[{self.pk}]):"
#             if state is not None:
#                 if self.state in [OrderState.FINISHED.value, OrderState.CANCELED.value]:
#                     log.warning(f"Rejecting update for {self} from {source} because state"
#                                 f" is {OrderState(self.state).name}")
#                     return False
#
#                 str_msg += f"\nstate: {OrderState(self.state).name} -> {OrderState(state).name}"
#                 if state != self.state:
#                     changed = True
#                     self.trade.add_comment(str_msg, from_log=False)
#                 self.state = state
#             if stop_price is not None:
#                 if not are_equal(stop_price, self.stop_price):
#                     changed = True
#                 str_msg += f"\nstop_price: {self.stop_price} -> {stop_price}"
#                 self.stop_price = stop_price
#             if price is not None:
#                 if not are_equal(price, self.price):
#                     changed = True
#                 str_msg += f"\nprice: {self.price} -> {price}"
#                 self.price = price
#             if fill_price is not None:
#                 if not are_equal(fill_price, self.fill_price):
#                     changed = True
#                 str_msg += f"\nfill_price: {self.fill_price} -> {fill_price}"
#                 self.fill_price = fill_price
#             if filled_quantity is not None and not are_equal(self.filled_quantity, filled_quantity):
#                 if not are_equal(filled_quantity, self.filled_quantity):
#                     changed = True
#                 str_msg += f"\nfilled_quantity: {self.filled_quantity} -> {filled_quantity}"
#                 self.filled_quantity = filled_quantity
#
#             if quantity is not None:
#                 if not are_equal(quantity, self.quantity):
#                     changed = True
#                 str_msg += f"\nquantity: {self.quantity} -> {quantity}"
#                 self.quantity = quantity
#
#             if commission_from_asset is not None:
#                 if not are_equal(quantity, self.commission_from_asset):
#                     changed = True
#                 str_msg += f"\ncommission_from_asset: {self.commission_from_asset} -> {commission_from_asset}"
#                 self.commission_from_asset = commission_from_asset
#
#             if twin is not None:
#                 changed = True
#                 str_msg += f"\ntwin: {self.twin} -> {twin}"
#                 self.twin = twin
#             try:
#                 self.save()
#                 str_msg += "\nSuccessfully saved\n"
#                 # print("Successfully saved ", self)
#
#             except Exception as e:
#                 log.exception(e, traceback, user=self)
#                 str_msg += f"\nFailed -> save due to:\n{e}\n"
#         if changed or force_log:
#             self.add_comment(str_msg, from_log=False)
#         # try:
#         #     if self.state == OrderState.FINISHED.value:
#         #         print("cancel_twin_order on ", self)
#         #         self.cancel_twin_order(source=f"{source} -> update_order_params")
#         #     print("cancel_if_twin_is_filled on ", self)
#         #     order.cancel_if_twin_is_filled()
#         # except Exception as e:
#         # transaction.commit()
#         return changed
#
#     def execute_order(self):
#         if self.state != OrderState.WAITING.value:
#             log.warning(f"{self} is not WAITING")
#             return
#         # if self.trade.is_bitmex():
#         #     return
#         if self.trade.is_binance():
#             from api.api_interface import BinanceInterface
#             if self.order_type == OrderType.LIMIT.value:
#                 return BinanceInterface.limit_order(trade=None, price=None, quantity=None, is_exit=None, order=self,
#                                                     commission_protected=True)
#         raise NotImplementedError("This type of order is not implemented for execute_order")
#
#     def last_update_in_seconds(self):
#         return (datetime.now().replace(tzinfo=None) - self.last_update.replace(tzinfo=None)).seconds
#
#     def is_updating(self):
#         t_delta = self.last_update_in_seconds()
#         if self.market.is_binance():
#             rand_timeout = random.randint(MAX_TIMEOUT_ORDER_BINANCE,
#                                           MAX_TIMEOUT_ORDER_BINANCE + MAX_TIMEOUT_ORDER_BINANCE // 2)
#             # print(self.id, " ", rand_timeout, " ", t_delta)
#             return t_delta < rand_timeout
#         return t_delta < MAX_TIMEOUT_ORDER
#
#     def get_unique_id(self):
#         if self.unique_id is not None:
#             return self.unique_id
#         self.unique_id = str(self.pk) + unique_order_id_concat
#         self.save()
#         return self.unique_id
#
#     def set_twins(self, order):
#         if order is None:
#             return
#         self.update_order_params(source="set_twins", twin=order)
#         order.update_order_params(source="set_twins", twin=self)
#
#     def short_str(self):
#         if self.stop_price is not None:
#             return f"Order[{self.pk}](Trade[{self.trade_id}])(stop={float(self.stop_price)})"
#         return f"Order[{self.pk}](Trade[{self.trade_id}])"
#
#     def __str__(self):
#         if self.trade is not None:
#             return f"Order[{self.pk}]({self.trade.mini_str()})"
#         else:
#             return f"Order[{self.pk}](trade=None)"
#
#     # def set_fill_price(self):
#     #     from api import api_interface
#     #     filled, fill_price, filled_quantity = api_interface.get_order_filled(trade=self.trade, order=self)
#     #     print("set_fill_price")
#     #     print(filled)
#     #     print(fill_price)
#     #     if filled:
#     #         self.fill_price = fill_price
#     #         self.filled_quantity = filled_quantity
#     #         self.save()
#
#     def is_exit_limit(self):
#         return self.order_type == OrderType.LIMIT.value and self.is_exit
#
#     def is_virtual_stop(self):
#         return self.order_type in [OrderType.VIRTUAL_STOP_LIMIT.value, OrderType.VIRTUAL_STOP_Market.value]
#
#     def reached_virtual_stop(self, price):
#         # maybe MODIFY later
#         if not self.is_virtual_stop():
#             return False
#         if self.is_exit:
#             if self.trade.signal.is_long():
#                 return price <= self.stop_price
#             else:
#                 return price >= self.stop_price
#         else:
#             if self.trade.signal.is_long():
#                 return price >= self.stop_price
#             else:
#                 return price <= self.stop_price
#
#     def new_stop_with_targets(self, price, strategy):
#         # MODIFY LATER: JOOOOOOB
#         if self.order_type == OrderType.MARKET.value:
#             log.warning("Called new_stop_with_targets for a MARKET order", add_to_file=True)
#             return None
#
#         if self.order_type not in [OrderType.STOP_MARKET.value, OrderType.VIRTUAL_STOP_Market.value,
#                                    OrderType.VIRTUAL_STOP_LIMIT.value]:
#             raise ValueError(f"unexpected order_type: {self.order_type}. Expected STOP_LIMIT or STOP_MARKET")
#
#         signal = self.trade.signal
#         targets = signal.get_targets()
#         hit = None
#         if signal.position == Position.LONG.value:
#             for target in targets:
#                 if price > target:
#                     hit = target
#                 else:
#                     break
#         else:
#             for target in targets:
#                 if price < target:
#                     hit = target
#                 else:
#                     break
#
#         if hit is None:
#             # log.info(f"No targets({targets[0]}) hit at price({price}) for {self.trade}", add_to_file=False)
#             return float(signal.stop_loss)
#
#         index = targets.index(hit)
#         progress = (index + 1) / len(targets)
#         # on first target reach, bring stop loss to entry zone
#         if index == 0:
#             return signal.symbol.normalize_price(float(self.trade.get_entry_price()))
#
#         distance = targets[index] - targets[index - 1]
#         coefficient = strategy.starting_coefficient + progress * (
#                 strategy.finishing_coefficient - strategy.starting_coefficient)
#
#         new_limit = hit - coefficient * distance
#         # log.debug(f"[NEW LIMIT](index: {index})(distance: {distance})(progress: {progress})"
#         #           f"(coefficient: {coefficient})(hit: {hit})(new_limit: {new_limit})")
#         return signal.symbol.normalize_price(new_limit)
#
#     def is_enter_order(self):
#         if self.state == OrderState.FINISHED.value and self.fill_price is not None:
#             return not self.is_exit
#         return False
#
#     def is_exit_order(self):
#         if self.state == OrderState.FINISHED.value and self.fill_price is not None:
#             return self.is_exit
#         return False
#
#     def is_maker(self):
#         if self.state == OrderState.FINISHED.value:
#             # modify: don't use == use is_close instead for floats
#             if self.fill_price == self.price:
#                 return True
#             return False
#         raise Exception("order is not FINISHED yet...")
#
#     def add_comment(self, comment, from_log=False):
#         if not from_log:
#             comment = datetime.now().replace(microsecond=0).__str__() + ": " + comment
#         comment = comment + "\n"
#         if self.comment is None:
#             self.comment = ""
#         self.comment = comment + self.comment
#         self.save()
#
#     def raise_error(self, e, propagate=True, notify_bot_add_file=True):
#         error_message = log.exception(
#             e, traceback, self.trade.profile, notify_bot=notify_bot_add_file, add_to_file=notify_bot_add_file)
#         if self.state != OrderState.RUNNING.value:
#             self.update_order_params(source=error_message, state=OrderState.ERROR.value)
#         self.add_error(error_message)
#         self.save()
#         if propagate:
#             self.trade.add_error("Order Error: order_id= %d\n%s" % (self.pk, error_message), from_log=True)
#         # DON'T CHANGE THIS. methods with True returns are considered to be done perfectly
#         return False
#
#     def add_error(self, error, from_log=False, with_trace=False):
#         if with_trace:
#             try:
#                 raise TraceException()
#             except TraceException:
#                 if not from_log:
#                     error = f"{datetime.now().replace(microsecond=0)}: {error}\n{traceback.format_exc()}"
#                     # error = datetime.now().replace(microsecond=0).__str__() + ": " + error + "\n" + str(
#                     #     traceback.format_exc()) + "\n"
#                 error = error + "\n"
#                 if self.error is None:
#                     self.error = ""
#                 self.error = error + self.error
#                 self.save()
#
#         else:
#             if not from_log:
#                 error = f"{datetime.now().replace(microsecond=0)}: {error}"
#             error = error + "\n"
#             if self.error is None:
#                 self.error = ""
#             self.error = f"{error}{self.error}"
#             self.save()
#
#     def update_order_state(self, force_api_call=False, notify_if_changed=True, warn_for_calling_api=True, source=""):
#         from api import api_interface
#         if force_api_call or (self.state in OrderState.get_active_states() and not self.is_updating()):
#             changed = api_interface.update_order_with_api(order=self, warn=warn_for_calling_api)
#             if changed and notify_if_changed:
#                 log.warning(f"======== API call by {source} changed DB {self}", add_to_file=True, notify_bot=True)
#
#     def is_in_active_state(self, force_api_call=False):
#         self.update_order_state(force_api_call=force_api_call, notify_if_changed=True,
#                                 warn_for_calling_api=True, source="is_in_active_state")
#         if self.state == OrderState.FINISHED.value:
#             self.cancel_twin_order(source=f"is_in_active_state_1")
#         return self.state in OrderState.get_active_states()
#
#     def cancel_if_twin_is_filled(self):
#         if self.twin is None:
#             return
#         if self.state not in OrderState.get_active_states():
#             log.debug_daily(f"cancel_if_twin_is_filled called for {self}. but state is not active")
#             return
#         if self.twin.state == OrderState.FINISHED.value:
#             self.cancel_order(cancel_order_from_twin=True, source="cancel_if_twin_is_filled")
#
#     def cancel_twin_order(self, source="PROCESS"):
#         # MODIFY:: if already canceled don't do anything
#         if self.twin is None:
#             return True
#         # if self.twin.state == OrderState.CANCELED.value:
#         #     self.twin.add_comment("Already CANCELED. Duplicate cancel-twin command aborted.", from_log=False)
#         #     return True
#         # if self.twin.state == OrderState.FINISHED.value:
#         #     self.twin.add_comment("Already FINISHED. Late cancel-twin command aborted.", from_log=False)
#         #     msg = log.error("unable to cancel twin-%s" % self.twin, add_to_file=True)
#         #     self.trade.add_error(msg, from_log=True)
#         #     # MODIFY: this can happen for other reasons than double-stops
#         #     self.trade.notify_user_of_double_stops(trade_id=self.trade.pk)
#         #     # This allows the brother to set it's own state to FINISHED
#         #     return True
#         msg = log.info("Canceling twin-order[%d] because order[%d] is filled" % (self.twin.pk, self.pk))
#         self.trade.add_comment(msg, from_log=True)
#         self.add_comment(msg, from_log=True)
#         cancel_success = self.twin.cancel_order(cancel_order_from_twin=True, source="cancel_twin_order_%s" % source)
#         if cancel_success:
#             msg = log.info("Twin-order canceled successfully", add_to_file=False)
#             self.trade.add_comment(msg, from_log=True)
#             return True
#         else:
#             msg = log.error("unable to cancel twin-%s" % self.twin, add_to_file=True)
#             self.trade.add_error(msg, from_log=True)
#             # MODIFY: MODIFIED: this can happen for other reasons than double-stops
#             # self.trade.notify_user_of_double_stops(trade_id=self.trade.pk)
#             return False
#
#     def cancel_order(self, source, cancel_order_from_twin=False):
#         # ASSUMPTION: Virtual orders are either WAITING or FINISHED; not RUNNING
#         # RUNNING orders get canceled through API
#         self.add_comment(f"Cancel command from {source} initiated...", from_log=False)
#         order = Order.objects.filter(pk=self.pk).select_for_update().get()
#         if order.order_type in [OrderType.VIRTUAL_STOP_Market.value, OrderType.VIRTUAL_STOP_LIMIT.value]:
#             order.update_order_params(state=OrderState.CANCELED.value, source="Virtual order CANCELED within DB")
#             return True
#
#         if order.state == OrderState.WAITING.value:
#             order.update_order_params(state=OrderState.CANCELED.value, source="order CANCELED from state=WAITING")
#             return True
#
#         if order.state == OrderState.CANCELED.value:
#             msg = log.warning(f"{self} is already CANCELED", add_to_file=False)
#             order.add_comment(msg, from_log=True)
#             return True
#         from api import api_interface
#         if order.state == OrderState.RUNNING.value:
#             response = api_interface.cancel_order_with_api(order.trade, order, source=source)
#             return response
#         if order.state == OrderState.FINISHED.value:
#             if cancel_order_from_twin:
#                 msg = log.error(
#                     f"Cancel command from twin order; but Order[{order.pk}] is already FINISHED")
#                 order.trade.add_error(msg, from_log=True)
#                 order.add_error(msg, from_log=True)
#                 return False
#         return True
#
#
# class OCO(models.Model):
#     side_choices = (
#         (BinanceOrderSide.SELL.value, BinanceOrderSide.SELL.name),
#         (BinanceOrderSide.BUY.value, BinanceOrderSide.BUY.name),
#     )
#
#     ListOrderStatus_choices = (
#         (OcoStatus.REJECT.value, OcoStatus.REJECT.name),
#         (OcoStatus.EXECUTING.value, OcoStatus.EXECUTING.name),
#         (OcoStatus.ALL_DONE.value, OcoStatus.ALL_DONE.name),
#     )
#
#     limit = models.OneToOneField(Order, on_delete=models.SET_NULL, related_name="limit", null=True)
#     stop = models.OneToOneField(Order, on_delete=models.SET_NULL, related_name="stop", null=True)
#     trade = models.ForeignKey(Trade, on_delete=models.SET_NULL, null=True)
#
#     is_exit = models.BooleanField(default=True)
#     side = models.CharField(max_length=15, choices=side_choices, default=BinanceOrderSide.SELL.value)
#
#     # list_status_type = models.CharField(max_length=127, null=True, choices=)
#     status_oco = models.CharField(max_length=127, null=True, choices=ListOrderStatus_choices)
#
#     timestamp = models.DateTimeField(auto_now_add=True)
#     trace = models.TextField(null=True, blank=True, default="")
#     list_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
#     last_update = models.DateTimeField(auto_now=True)
#     last_update_with_exchange = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"OCO[{self.pk}]({self.trade.mini_str()})"
#
#     def cancel_oco(self):
#         if self.status_oco == OcoStatus.EXECUTING.value:
#             from api.api_interface import BinanceInterface
#             BinanceInterface.delete_oco(self)
#         else:
#             msg = log.warning(f"{self} cancel_oco aborted (not in EXECUTING state).")
#             self.add_trace(msg, from_log=True)
#
#     def update_state(self, next_state, source):
#         trace = f"[{source}] state: {self.status_oco} -> {next_state}"
#         self.status_oco = next_state
#         self.add_trace(trace)
#         self.save()
#
#     def update_status_if_expired(self, warn_for_update, expiry_seconds=MAX_TIMEOUT_ORDER_BINANCE):
#         if datetime.now() - self.last_update_with_exchange > timedelta(seconds=expiry_seconds):
#             self.update_with_api(warn_for_update=warn_for_update)
#
#     def update_status(self):
#         if datetime.now() - self.last_update_with_exchange > timedelta(seconds=MAX_TIMEOUT_ORDER_BINANCE):
#             self.update_with_api()
#
#     def update_with_api(self, warn_for_update=False):
#         if warn_for_update:
#             log.warning(f"querying {self} with API", notify_bot=True)
#         from api.api_interface import BinanceInterface
#         BinanceInterface.query_oco(self)
#         self.last_update_with_exchange = datetime.now()
#         self.save()
#
#     def update_with_json_response(self, response, source):
#         self.update_state(next_state=response['listOrderStatus'], source=source)
#         if 'orderReports' not in response:
#             return
#         for order in response.get('orderReports'):
#             if order['type'] == "LIMIT_MAKER":
#                 self.limit.update_binance_order_with_json(
#                     response=order,
#                     source=source)
#             elif order['type'] == "STOP_LOSS_LIMIT":
#                 self.stop.update_binance_order_with_json(
#                     response=order,
#                     source=source)
#             else:
#                 log.error(f"{self} response included unexpected type of order: {order['type']}", notify_bot=True)
#
#     def add_trace(self, trace, from_log=False):
#         if not from_log:
#             trace = datetime.now().replace(microsecond=0).__str__() + ": " + trace
#         trace = trace + "\n"
#         self.trace = trace + self.trace
#         self.save()
#
#     @staticmethod
#     def create_oco(trade, quantity, price, stop_price, stop_limit_price, side=BinanceOrderSide.SELL.value):
#         if side == BinanceOrderSide.SELL.value:
#             if price < stop_price:
#                 raise ValueError("price must be more than stop in SELL oco")
#         else:
#             if price > stop_price:
#                 raise ValueError("price must be less than stop in BUY oco")
#
#         limit = Order.objects.create(
#             trade=trade,
#             market=trade.signal.market,
#             order_type=OrderType.LIMIT.value,
#             is_exit=True,
#             quantity=quantity,
#             price=price,
#             oco_order=True)
#         limit.get_unique_id()
#         stop = Order.objects.create(
#             order_type=OrderType.STOP_LIMIT.value,
#             trade=trade,
#             market=trade.signal.market,
#             is_exit=True,
#             quantity=quantity,
#             stop_price=stop_price,
#             price=stop_limit_price,
#             oco_order=True)
#
#         oco = OCO.objects.create(
#             limit=limit,
#             stop=stop,
#             trade=trade,
#         )
#         return oco
#
#     def get_list_id(self):
#         if self.list_id is not None:
#             return self.list_id
#         self.list_id = f"{unique_list_id_concat}{self.pk}"
#         self.save()
#         return self.list_id
#
#
# class Credit(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
#     total_amount = models.DecimalField(max_digits=20, decimal_places=8, null=False, blank=True)
#     free_amount = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
#     freeze_amount = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
#     currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=False)
#     market = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True, blank=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     # def update_or_create_credit(self):
#     #     pass
#
#
# class AutoTrade(models.Model):
#     profile = models.ForeignKey("accounts.Profile", on_delete=models.SET_NULL, null=True, blank=False)
#     market = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True, blank=False)
#
#     generic = models.BooleanField(default=False)
#     base = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
#     symbol = models.ForeignKey(Symbol, on_delete=models.SET_NULL, null=True, blank=True)
#
#     strategy = models.ForeignKey(Strategy, on_delete=models.SET_NULL, null=True, blank=False)
#     enabled = models.BooleanField(default=False)
#     channel = models.ForeignKey(SignalChannel, on_delete=models.SET_NULL, null=True, blank=False)
#     quote_amount_at_stake = models.DecimalField(max_digits=16, decimal_places=8, null=True, blank=True)
#     manage_risk = models.BooleanField(default=False, help_text="Set true for risk_amount_usd effective")
#     quote_amount_at_risk = models.DecimalField(max_digits=16, decimal_places=8, blank=True, null=True)
#     # test = models.BooleanField(default=False)
#     mini = models.BooleanField(default=False)
#     # type_of_amount = models.PositiveSmallIntegerField(choices=Choices.auto_trade_creator_type,
#     #                                                   default=AutoTradeCreatorType.Number.value)
#     last_editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     pyramid = models.SmallIntegerField(default=0, help_text="set 0 to bypass")
#     trace = models.TextField(null=True, blank=True, default="")
#
#     class Meta:
#         unique_together = ('profile', 'market', 'symbol', 'mini', 'strategy', 'channel', 'base')
#
#     def add_trace(self, trace, from_log=False):
#         if not from_log:
#             trace = datetime.now().replace(microsecond=0).__str__() + ": " + trace
#         trace = trace + "\n"
#         if self.trace is None:
#             self.trace = ""
#         self.trace = trace + self.trace
#         self.save()
#
#     def clean(self):
#         if self.generic:
#             if self.base is None:
#                 raise ValidationError("'base' is a mandatory parameter for generic auto_trades")
#             if self.symbol is not None:
#                 raise ValidationError("'symbol' must be blank for generic auto_trades")
#         else:
#             if self.symbol is None:
#                 raise ValidationError("'symbol' is a mandatory parameter for non-generic auto_trades")
#             if self.base is not None:
#                 raise ValidationError("'base' must be blank for non-generic auto_trades")
#
#         if self.manage_risk:
#             if self.quote_amount_at_risk is None:
#                 raise ValidationError("'quote_amount_in_risk' is a mandatory parameter for risk management")
#             if self.quote_amount_at_stake is not None:
#                 raise ValidationError("'quote_amount_at_stake' must be blank for for risk management")
#         else:
#             # amount is also checked here for non-risk management trades
#             if self.quote_amount_at_stake is None:
#                 raise ValidationError("'quote_amount_at_stake' is a mandatory parameter for risk management")
#             if self.quote_amount_at_risk is not None:
#                 raise ValidationError("'quote_amount_in_risk' must be blank for for risk management")
#             if self.generic:
#                 min_notional_set = Symbol.objects.filter(second=self.base, active=True, market=self.market
#                                                          ).aggregate(Max('minimum_order_quote_size'))
#                 min_notional = 0
#                 for key, value in min_notional_set.items():
#                     min_notional = value
#                     break
#             else:
#                 min_notional = self.symbol.minimum_order_quote_size
#             practical_min_notional = round(min_notional * Decimal(PRACTICAL_MIN_NOTIONAL_INDEX), 8)
#             if self.quote_amount_at_stake < practical_min_notional:
#                 raise ValidationError(
#                     f"Quote amount at stake ({float(self.quote_amount_at_stake)} {self.get_base()}) < "
#                     f"practical minimum order value ({float(practical_min_notional)} {self.get_base()})")
#
#     @staticmethod
#     def create_trade_for_matching_auto_trades(signal):
#         auto_trades = AutoTrade.objects.filter(
#             generic=False, symbol=signal.symbol,
#             market=signal.market, enabled=True, mini=signal.mini, channel=signal.channel)
#         generic_auto_trades = AutoTrade.objects.filter(
#             generic=True, base=signal.symbol.second,
#             market=signal.market, enabled=True, mini=signal.mini, channel=signal.channel)
#
#         for auto_trade in auto_trades | generic_auto_trades:
#             try:
#                 auto_trade.create_trade(signal=signal)
#             except Exception as e:
#                 msg = log.exception(e, traceback, auto_trade.profile)
#                 auto_trade.add_trace(msg, from_log=True)
#
#     def create_trade(self, signal):
#         if not isinstance(signal, Signal):
#             return
#         if not self.profile.exchangeaccount_set.get(market=signal.market).enable:
#             msg = log.debug_daily(
#                 f"Did not create trade for {self.profile} with {signal} because account is not enabled.")
#             self.add_trace(msg, from_log=True)
#             return
#         if self.profile.is_bot_trader():
#             if not self.profile.get_active_membership():
#                 msg = log.debug_daily(
#                     f"Did not create trade for {self.profile} with {signal} user does not have get_active_membership")
#                 self.add_trace(msg, from_log=True)
#                 return
#             if not self.profile.active_subscription(analyst=signal.channel.creator_profile):
#                 msg = log.debug_daily(
#                     f"Did not create trade for {self.profile} with {signal} user does not have active_subscription")
#                 self.add_trace(msg, from_log=True)
#                 return
#         price = Decimal(signal.symbol.father_get_price(is_long=signal.is_long(), is_exit=False))
#         if signal.is_in_entry_zone(price):
#             supposed_entry_price = price
#         else:
#             supposed_entry_price = signal.closer_side_of_entry_zone(price)
#
#         if self.manage_risk:
#
#             distance_to_stop = abs(float(supposed_entry_price) - float(signal.stop_loss))
#             margin = float(distance_to_stop) / float(supposed_entry_price)
#             quote_at_stake = float(self.quote_amount_at_risk) / margin
#             quantity = signal.symbol.get_quantity_from_quote_at_stake(quote_at_stake, price=supposed_entry_price)
#
#             msg = log.info(
#                 f"AutoTrade[{self.pk}] set quantity({float(quantity)}) with "
#                 f"{self.quote_amount_at_risk} {self.get_base()} at risk ({quote_at_stake} {self.get_base()} at stake)\n"
#                 f"margin({margin}) price({price}) entry({supposed_entry_price})")
#         else:
#             quantity = signal.symbol.get_quantity_from_quote_at_stake(self.quote_amount_at_stake,
#                                                                       price=supposed_entry_price)
#             msg = log.info(f"AutoTrade set quantity ({float(quantity)}) "
#                            f"with {float(self.quote_amount_at_stake)} {self.get_base()} at stake ({signal.symbol}:{supposed_entry_price}).")
#
#         state = TradeState.WAITING.value
#         # check pyramiding
#         if self.pyramid > 0:
#             concurrent_trades = Trade.objects.filter(auto_trade=self, state__in=TradeState.get_active_states())
#             if len(concurrent_trades) >= self.pyramid:
#                 state = TradeState.CANCELED.value
#                 msg = log.info(f"Pyramiding prevented trade from execution. state=CANCELED\n{msg}")
#         trade = Trade(
#             # MODIFY: delete user
#             profile=self.profile,
#             signal=signal,
#             strategy=self.strategy,
#             quantity=quantity,
#             state=state,
#             comment=msg,
#             auto_trade=self
#         )
#         try:
#             trade.save()
#             self.add_trace(f"Successfully created trade on {signal}")
#         except ValidationError as e:
#             log.error(f"Validation error on saving trade generated by AutoTrade({self}) triggered by {signal}:\n{e}")
#             self.add_trace(f"Failed to create trade on {signal} due to:\n{e}")
#             return False
#         return trade
#
#     def get_base(self):
#         if self.generic:
#             return self.base
#         return self.symbol.second
#
#     def __str__(self):
#         # return "%s on %s" % (self.profile, self.)
#         if self.generic:
#             target = f"---{self.base}"
#         else:
#             target = f"{self.symbol}"
#
#         return f"AutoT[{self.pk}] {self.profile} on {self.market} for {target}"
#         # return self.profile.__str__() + ": " + self.market.__str__() + "/" + self.symbol.__str__()

class SignalResult(models.Model):
    signal = models.ForeignKey(Signal, on_delete=models.SET_NULL, null=True)
    profit = models.CharField(max_length=255)
    first_target_profit = models.CharField(max_length=255)
    has_won = models.BooleanField()




