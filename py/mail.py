# monitors packages. Should be used only in a private channel. Make private thread?

from os import strerror
from discord.ext import commands
import discord
import shippo
import requests
import pickle
import asyncio
import obj.private_user_data
from exceptions import ShippyError

class TrackRequest:
    def __init__(self, requester : discord.User, nickname : str, resp_obj : requests.Response):
        self.requester = requester
        self.nickname = nickname
        self.resp_obj = resp_obj

class Shippy():
    supported_carriers = {
        'APC Postal' : 'apc_postal',
        'Aramex' : 'aramex',
        'Asendia US' : 'asendia_us',
        'Australia Post' : 'australia_post',
        'Axlehire' : 'axlehire',
        'BorderGuru' : 'borderguru',
        'Boxberry' : 'boxberry',
        'Bring' : 'bring',
        'Canada Post' : 'canada_post',
        'CDL' : 'cdl',
        'CollectPlus' : 'collect_plus',
        'CorreiosBR' : 'correios_br',
        'Correos Espana' : 'correos_espana',
        'Couriers Please' : 'couriersplease',
        'Deutsche Post' : 'deutsche_post',
        'DHL Benelux' : 'dhl_benelux',
        'DHL eCommerce' : 'dhl_ecommerce',
        'DHL Express' : 'dhl_express',
        'DHL Germany C2C' : 'dhl_germany_c2c',
        'DHL Germany' : 'dhl_germany',
        'DPD GERMANY' : 'dpd_germany',
        'DPD' : 'dpd',
        'DPD UK' : 'dpd_uk',
        'Estafeta' : 'estafeta',
        'Fastway Australia' : 'fastway_australia',
        'FedEx' : 'fedex',
        'Globegistics' : 'globegistics',
        'GLS Deutschland' : 'gls_deutschland',
        'GLS France' : 'gls_france',
        'GLS US' : 'gls_us',
        'Gophr' : 'gophr',
        'GSO' : 'gso',
        'Hermes Germany B2C' : 'hermes_germany_b2c',
        'Hermes UK' : 'hermes_uk',
        'Hongkong Post' : 'hongkong_post',
        'LaserShip' : 'lasership',
        'LSO' : 'lso',
        'Mondial Relay' : 'mondial_relay',
        'Newgistics' : 'newgistics',
        'New Zealand Post' : 'new_zealand_post',
        'Nippon Express' : 'nippon_express',
        'OnTrac' : 'ontrac',
        'OrangeDS' : 'orangeds',
        'Parcelforce' : 'parcelforce',
        'Parcel' : 'parcel',
        'Passport' : 'passport',
        'PCF' : 'pcf',
        'Posti' : 'posti',
        'Purolator' : 'purolator',
        'Royal Mail' : 'royal_mail',
        'RR Donnelley' : 'rr_donnelley',
        'Russian Post' : 'russian_post',
        'Sendle' : 'sendle',
        'SkyPostal' : 'skypostal',
        'Stuart' : 'stuart',
        'UPS' : 'ups',
        'USPS' : 'usps',
        'Yodel' : 'yodel',
    }

    token = obj.private_user_data.Token.mail_token
    shippo.config.api_key = token
 
    @classmethod
    async def fetch_data(cls, carrier : str, track_number : str):
        '''Takes in carrier and track number and attempts to
        retrieve the parcel datastructure from shippo'''

        headers = {
            'Authorization' : 'ShippoToken ' + str(cls.token)
        }

        # Find which carrier regardless of capitalization usage
        # If none found, return carrier error
        inc = 0
        valid_key = ''
        carrier_keys = cls.supported_carriers.keys()
        for key in carrier_keys:
            if key.lower() == carrier.lower():
                valid_key = key
                break
            elif inc == len(carrier_keys) - 1:
                raise ShippyError('{} is an invalid carrier. Please refer to https://goshippo.com/docs/reference#carriers for list of valid carriers.'.format(carrier))
            inc += 1

        url_carrier = cls.supported_carriers[valid_key]                
        shippo_url = 'https://api.goshippo.com/tracks/' + url_carrier + '/' + track_number
        try:
            shippo_data = requests.get(shippo_url, headers=headers, timeout=3)
        except requests.exceptions.Timeout:
            raise ShippyError('{} is an invalid tracking number for {}.'.format(track_number, valid_key))
        else:
            return shippo_data


class Mail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # await self.check_file_for_update()

    async def cog_command_error(self, ctx:commands.Context, error:commands.CommandError):
        await ctx.send('An error occurred:{}'.format(str(error)))

    def unpickle_all_mail(self):
        '''Unpickles mail data as generator object.'''

        with open('obj/track_data.pkl', 'rb') as dta:
            while True:
                try:
                    yield pickle.load(dta)
                except EOFError:
                    break

    def update_pickle_mail(self, *updated_objs):
        '''Replaces entire pickle file with list of updated objects.'''

        with open('obj/track_data.pkl', 'wb') as dta:
            for obj in updated_objs:
                pickle.dump(obj, dta)

    def unlog_pickle_mail(self, *file_data, track_number : str):
        '''Unlogs package from pickle.'''

        # Update the pickle without the found tracking number.
        # This method should only be called upon verification that the tracking
        # number has been found so there is no check for it not existing
        processed_file_data = []
        for obj in file_data:
            if obj.resp_obj.tracking_number != track_number:
                processed_file_data.append(obj)

        self.update_pickle_mail(processed_file_data)

    async def check_file_for_update(self):
        '''Looks up data based on pickle file content. Sends update messages to relevant authors if necessary.'''

        while True:
            # Create generator for pickle objects.
            # For each object, if update times are different, update object.
            # Send message to author.
            # Else, Do nothing. 
            # Afterwards, append object whether updated or not to be repickled

            track_requests = self.unpickle_all_mail()
            verified_track_requests = []
            for track_req in track_requests:
                carrier = track_req.resp_obj.carrier
                tracking_number = track_req.resp_obj.tracking_number

                inet_data = await Shippy.fetch_data(carrier, tracking_number)

                file_date = track_req.resp_obj.tracking_status.status_date
                if file_date != inet_data.tracking_status.status_date:
                    track_req.resp_obj = inet_data
                    
                    identifer = ''
                    if track_req.nickname is not None:
                        identifer = track_req.nickname
                    else:
                        identifer = tracking_number
                    await track_req.requester.send('Your Tracking {} with {} has updated!'.format(identifer, carrier))
                
                verified_track_requests.append(track_req.resp_obj)
            self.update_pickle_mail(verified_track_requests)
            await asyncio.sleep(3600)   # Pause for an hour

    @commands.command()
    async def track(self, ctx : commands.Context, carrier : str, track_number : str):
        '''Syntax: CMD Carrier Trk# PkgNm'''
        # Check file to make sure tracking number is not already being tracked.
        # If cURL valid, Write carrier, tracking number, and info to file
        # Calls info-display command if there is an update.

        arg = ctx.message.content.split(' ')
        carrier = arg[1]
        track_number = arg[2]
        package_name = arg[3]

        # Retrieve data.
        # If there is no old data, paste data to file.
        # Else, compare new data with old data.
        # If matching, do nothing. Else, send message and paste data to file.
        inet_data = Shippy.fetch_data(carrier, track_number)
        file_data = self.unpickle_all_mail()
        total_obj = []
        for object in file_data:
            if object.tracking_number == inet_data.tracking_number and object.carrier == inet_data.carrier:
                if object.tracking_status.status_date != inet_data.tracking_status.status_date:
                    total_obj.append(inet_data)
                else:
                    total_obj.append(object)
            else:
                total_obj.append(object)
        self.update_pickle_mail(total_obj)

    # untrack package
    @commands.command()
    async def untrack(self, ctx, track_number : str):
        '''Untracks package.'''

        file_data = self.unpickle_all_mail()
        processed_file_data = []
        is_found = False
        for obj in file_data:
            processed_file_data.append(obj)
            if obj.resp_obj.tracking_number == track_number:
                if obj.requester.id != ctx.author.id:
                    raise ShippyError('You do not have the permission to untrack this package.')
                else:
                    is_found = True

        if is_found:
            self.unlog_pickle_mail(processed_file_data, track_number)
        else:
            raise ShippyError('Tracking number is currently not being logged.')
                

def setup(bot: commands.Bot):
    bot.add_cog(Mail(bot))
