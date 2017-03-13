"""
A Skeleton EDMC Plugin
"""
import locale
import sys

import Tkinter

this = sys.modules[__name__]
locale.setlocale(locale.LC_ALL, '')


def plugin_start():
    """
    Start this plugin
    :return: Plugin name
    """
    return 'EDMC_Bounty_Tracker'


def plugin_app(parent):
    """
    Return a TK Widget for the EDMC main window.
    :param parent:
    :return:
    """
    label = Tkinter.Label(parent, text="Bounty:")
    this.status = Tkinter.Label(parent, anchor=Tkinter.W, text="0 CR")
    this.total_bounty = 0
    return label, this.status


def journal_entry(cmdr, system, station, entry):
    """
    E:D client made a journal entry
    :param cmdr: The Cmdr name, or None if not yet known
    :param system: The current system, or None if not yet known
    :param station: The current station, or None if not docked or not yet known
    :param entry: The journal entry as a dictionary
    :return:
    """
    if entry['event'] == 'Bounty':
        # We collected a bounty
        reward = entry['TotalReward']
        this.total_bounty += reward
        val = locale.format("%d", this.total_bounty, grouping=True)
        this.status['text'] = '{0} CR'.format(val)
    if entry['event'] == 'RedeemVoucher' and entry['Type'] == 'bounty':
        # We redeemed one or more bounties, remove them from our count
        redeemed = entry['Amount']
        this.total_bounty -= redeemed
        if this.total_bounty < 0:
            # If there are bounties we didn't know about
            this.total_bounty = 0
        val = locale.format("%d", this.total_bounty, grouping=True)
        this.status['text'] = '{0} CR'.format(val)
    if entry['event'] == 'Died':
        this.total_bounty = 0
        this.status['text'] = '0 CR'

