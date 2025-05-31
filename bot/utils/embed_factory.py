
"""
Emerald's Killfeed - Embed Factory
Creates consistent, themed embeds with proper thumbnail placement and no emojis
"""

import logging
import discord
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class EmbedFactory:
    """
    Factory for creating themed embeds with consistent styling
    - All embeds use proper logo thumbnails on the right side
    - No emojis are used in any embeds
    - Consistent color theming
    - File attachments for assets
    """
    
    # Theme colors
    COLORS = {
        'connection': 0x00d38a,  # Green for connections
        'killfeed': 0xff6b6b,   # Red for killfeed
        'mission': 0x4ecdc4,    # Teal for missions
        'airdrop': 0xffd93d,    # Gold for airdrops
        'helicrash': 0xff8c42,  # Orange for helicrash
        'trader': 0x6c5ce7,     # Purple for trader
        'vehicle': 0x74b9ff,    # Blue for vehicles
        'bounty': 0xe84393,     # Pink for bounties
        'economy': 0x00b894,    # Green for economy
        'leaderboard': 0x0984e3, # Blue for leaderboard
        'error': 0xe74c3c,      # Red for errors
        'success': 0x27ae60,    # Green for success
        'warning': 0xf39c12,    # Orange for warnings
        'info': 0x3498db        # Blue for info
    }
    
    # Asset paths
    ASSETS_PATH = Path('./assets')
    
    # Asset mappings
    ASSETS = {
        'connection': 'Connections.png',
        'killfeed': 'Killfeed.png',
        'mission': 'Mission.png',
        'airdrop': 'Airdrop.png',
        'helicrash': 'Helicrash.png',
        'trader': 'Trader.png',
        'vehicle': 'Vehicle.png',
        'bounty': 'Bounty.png',
        'economy': 'Gamble.png',
        'leaderboard': 'Leaderboard.png',
        'faction': 'Faction.png',
        'weapon': 'WeaponStats.png',
        'suicide': 'Suicide.png',
        'falling': 'Falling.png',
        'main': 'main.png'
    }

    # Themed messages for each embed type
    THEMED_MESSAGES = {
        'connection_join': [
            ("Reinforcements Arrive", "A new operative has entered the battlefield"),
            ("Squad Member Online", "Fresh backup has joined the mission"),
            ("New Arrival Detected", "Another survivor enters the hostile zone"),
            ("Operative Deployment", "Military personnel now active in the field"),
            ("Backup Has Arrived", "Additional support is now operational"),
            ("New Fighter Enlisted", "Another warrior joins the conflict"),
            ("Mercenary Activated", "A hired gun has entered the combat zone"),
            ("Soldier Reporting In", "Military unit now deployed and ready"),
            ("Combat Unit Online", "Tactical operator is now field-ready"),
            ("Fresh Blood Arrives", "New combatant has entered the warzone")
        ],
        'connection_leave': [
            ("Extraction Confirmed", "Operative has successfully left the battlefield"),
            ("Squad Member Offline", "Team member has concluded their mission"),
            ("Departure Logged", "Fighter has withdrawn from the combat zone"),
            ("Mission Complete", "Operative extraction has been completed"),
            ("Radio Silence", "Communication lost with field operative"),
            ("Tactical Withdrawal", "Strategic retreat executed successfully"),
            ("End of Deployment", "Tour of duty has been concluded"),
            ("Evacuation Complete", "Personnel safely removed from danger zone"),
            ("Mission Concluded", "Operative has finished their assignment"),
            ("Fade to Black", "Last transmission received from departing unit")
        ],
        'killfeed_kill': [
            ("Hostile Eliminated", "Another survivor has fallen to superior tactics"),
            ("Combat Victory", "The wasteland claims another warrior"),
            ("Kill Confirmed", "Survival of the fittest in action"),
            ("Target Down", "One less threat in the contaminated zone"),
            ("Elimination Recorded", "The strong prey upon the weak"),
            ("Hostile Neutralized", "Another soul lost to the harsh reality"),
            ("Combat Success", "Violence solves yet another dispute"),
            ("Enemy Down", "The apocalypse continues to thin the herd"),
            ("Confirmed Kill", "Natural selection at its finest"),
            ("Threat Eliminated", "The wasteland's brutal law prevails")
        ],
        'killfeed_suicide': [
            ("Manual Uninstall", "Someone pressed the wrong button, it didn't end well"),
            ("Critical Error", "Task failed successfully, permanently"),
            ("Self-Service Checkout", "Took the express lane to the afterlife"),
            ("User Malfunction", "Hardware failure: operator not included"),
            ("Instant Karma", "When life gives you grenades, don't pull the pin"),
            ("Oops Moment", "That wasn't the reload button"),
            ("Final Bug Report", "Error 404: Player not found"),
            ("Creative Problem Solving", "Found a permanent solution to temporary problems"),
            ("Unscheduled Logout", "Rage quit taken to the extreme"),
            ("Self-Destruct Sequence", "Someone skipped the safety briefing")
        ],
        'killfeed_fall': [
            ("Gravity Check Failed", "Physics had different ideas about that flight plan"),
            ("Unexpected Landing", "Ground came up faster than expected"),
            ("Terminal Velocity Achieved", "Discovered the hard way that humans can't fly"),
            ("Altitude Adjustment", "What goes up, comes down... hard"),
            ("Flight Plan Rejected", "Air traffic control: Gravity"),
            ("Gravity Assisted Exit", "Isaac Newton's law still applies in the apocalypse"),
            ("Rapid Descent Protocol", "Took the scenic route down"),
            ("Uncontrolled Landing", "Forgot to pack a parachute for that trip"),
            ("Ground Impact Event", "Learned that falling with style still hurts"),
            ("Elevation Miscalculation", "Overestimated their frequent flyer miles")
        ],
        'mission_ready': [
            ("Objective Available", "New tactical mission is ready for deployment"),
            ("Mission Briefing", "High-value target area now accessible"),
            ("Operation Greenlight", "Strategic objective cleared for engagement"),
            ("Target Acquired", "Priority mission zone now active"),
            ("Go Signal Received", "Mission parameters have been established"),
            ("Deployment Authorized", "Tactical operation ready for execution"),
            ("Mission Active", "Strategic objective is now operational"),
            ("Objective Online", "Target zone cleared for engagement"),
            ("Operation Commenced", "Mission parameters are now live"),
            ("Battle Orders", "Tactical engagement zone is active")
        ],
        'airdrop_incoming': [
            ("Supply Drop Inbound", "Aerial resupply package approaching"),
            ("Cargo Drop Detected", "Supply aircraft on final approach"),
            ("Air Support Incoming", "Logistics drop confirmed inbound"),
            ("Supply Bird Approaching", "Aerial cargo delivery in progress"),
            ("Package Delivery", "High-altitude supply drop initiated"),
            ("Resupply Mission", "Aerial logistics package incoming"),
            ("Sky Delivery", "Supply aircraft making final approach"),
            ("Cargo Inbound", "Aerial resupply mission in progress"),
            ("Supply Drop Active", "Logistics delivery now approaching"),
            ("Air Logistics", "Supply package incoming from above")
        ],
        'helicrash_event': [
            ("Aircraft Down", "Helicopter has crash-landed in the area"),
            ("Emergency Landing", "Rotorcraft made unscheduled ground contact"),
            ("Heli Down", "Aviation incident has been reported"),
            ("Crash Site Active", "Helicopter wreckage detected"),
            ("Bird Down", "Rotary aircraft suffered catastrophic failure"),
            ("Emergency Descent", "Helicopter made forced landing"),
            ("Aviation Incident", "Rotorcraft emergency landing confirmed"),
            ("Chopper Down", "Helicopter crash site now active"),
            ("Flight Emergency", "Aviation emergency landing reported"),
            ("Rotor Failure", "Helicopter suffered mechanical failure")
        ],
        'trader_arrival': [
            ("Black Market Open", "Underground dealer has arrived"),
            ("Merchant Arrival", "Independent trader now conducting business"),
            ("Dealer Active", "Black market vendor is open for trade"),
            ("Trade Opportunity", "Special merchant has arrived"),
            ("Underground Market", "Illegal arms dealer now available"),
            ("Contraband Available", "Black market trader is open"),
            ("Shadow Merchant", "Underground dealer conducting business"),
            ("Arms Dealer Active", "Weapons merchant now available"),
            ("Black Market Vendor", "Illegal trader has set up shop"),
            ("Underworld Trading", "Shadow market is now operational")
        ]
    }

    @classmethod
    def _get_themed_message(cls, message_type: str, index: int = None) -> Tuple[str, str]:
        """Get a themed message for the given type"""
        import random
        
        messages = cls.THEMED_MESSAGES.get(message_type, [("System Message", "Event occurred")])
        
        if index is not None and 0 <= index < len(messages):
            return messages[index]
        
        # Return random themed message
        return random.choice(messages)

    @classmethod
    async def build_connection_embed(cls, data: Dict[str, Any]) -> Tuple[discord.Embed, Optional[discord.File]]:
        """Build themed connection embed"""
        try:
            # Determine if join or leave
            is_join = 'arrive' in data.get('title', '').lower() or 'reinforcements' in data.get('title', '').lower()
            message_type = 'connection_join' if is_join else 'connection_leave'
            
            # Get themed message
            title, description = cls._get_themed_message(message_type)
            
            # Create embed
            color = cls.COLORS['connection']
            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )
            
            # Add fields
            player_name = data.get('player_name', 'Unknown Player')
            platform = data.get('platform', 'Unknown')
            server_name = data.get('server_name', 'Unknown Server')
            
            embed.add_field(name="Player", value=player_name, inline=True)
            embed.add_field(name="Platform", value=platform, inline=True)
            embed.add_field(name="Server", value=server_name, inline=True)
            
            # Set thumbnail
            asset_path = cls.ASSETS_PATH / cls.ASSETS['connection']
            file_attachment = None
            if asset_path.exists():
                file_attachment = discord.File(str(asset_path), filename=cls.ASSETS['connection'])
                embed.set_thumbnail(url=f"attachment://{cls.ASSETS['connection']}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed, file_attachment
            
        except Exception as e:
            logger.error(f"Failed to build connection embed: {e}")
            return cls._create_fallback_embed("Connection Event", "Player activity recorded")

    @classmethod
    async def build_killfeed_embed(cls, data: Dict[str, Any]) -> Tuple[discord.Embed, Optional[discord.File]]:
        """Build themed killfeed embed"""
        try:
            is_suicide = data.get('is_suicide', False)
            weapon = data.get('weapon', 'Unknown')
            
            # Determine message type
            if is_suicide:
                if 'fall' in weapon.lower() or 'falling' in weapon.lower():
                    message_type = 'killfeed_fall'
                else:
                    message_type = 'killfeed_suicide'
            else:
                message_type = 'killfeed_kill'
            
            # Get themed message
            title, description = cls._get_themed_message(message_type)
            
            # Create embed
            color = cls.COLORS['killfeed']
            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )
            
            if is_suicide:
                # Suicide embed
                player_name = data.get('victim', data.get('player_name', 'Unknown'))
                embed.add_field(name="Player", value=player_name, inline=True)
                embed.add_field(name="Cause", value=weapon, inline=True)
                
                # Use appropriate asset
                asset_name = 'falling.png' if 'fall' in weapon.lower() else 'suicide.png'
            else:
                # Kill embed
                killer = data.get('killer', 'Unknown')
                victim = data.get('victim', 'Unknown')
                distance = data.get('distance', 0)
                
                embed.add_field(name="Killer", value=killer, inline=True)
                embed.add_field(name="Victim", value=victim, inline=True)
                embed.add_field(name="Weapon", value=weapon, inline=True)
                
                if distance and float(distance) > 0:
                    embed.add_field(name="Distance", value=f"{distance}m", inline=True)
                    
                asset_name = 'killfeed.png'
            
            # Set thumbnail
            asset_path = cls.ASSETS_PATH / asset_name
            file_attachment = None
            if asset_path.exists():
                file_attachment = discord.File(str(asset_path), filename=asset_name)
                embed.set_thumbnail(url=f"attachment://{asset_name}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed, file_attachment
            
        except Exception as e:
            logger.error(f"Failed to build killfeed embed: {e}")
            return cls._create_fallback_embed("Combat Event", "Combat activity recorded")

    @classmethod
    async def build_mission_embed(cls, data: Dict[str, Any]) -> Tuple[discord.Embed, Optional[discord.File]]:
        """Build themed mission embed"""
        try:
            # Get themed message
            title, description = cls._get_themed_message('mission_ready')
            
            # Create embed
            level = data.get('level', 1)
            if level >= 5:
                color = 0xff0000  # Red for highest level
            elif level >= 4:
                color = 0xff8c00  # Orange for high level
            elif level >= 3:
                color = 0xffd700  # Gold for medium level
            else:
                color = cls.COLORS['mission']  # Default teal for low level
            
            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )
            
            # Add mission details
            mission_id = data.get('mission_id', '')
            mission_name = cls.normalize_mission_name(mission_id)
            state = data.get('state', 'READY')
            
            embed.add_field(name="Mission", value=mission_name, inline=False)
            embed.add_field(name="Difficulty Level", value=f"Level {level}", inline=True)
            embed.add_field(name="Status", value=state.replace('_', ' ').title(), inline=True)
            
            # Set thumbnail
            asset_path = cls.ASSETS_PATH / cls.ASSETS['mission']
            file_attachment = None
            if asset_path.exists():
                file_attachment = discord.File(str(asset_path), filename=cls.ASSETS['mission'])
                embed.set_thumbnail(url=f"attachment://{cls.ASSETS['mission']}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed, file_attachment
            
        except Exception as e:
            logger.error(f"Failed to build mission embed: {e}")
            return cls._create_fallback_embed("Mission Update", "Mission status changed")

    @classmethod
    async def build(cls, embed_type: str, data: Dict[str, Any]) -> Tuple[discord.Embed, Optional[discord.File]]:
        """
        Build a complete embed with proper thumbnail and file attachment
        Returns tuple of (embed, file_attachment)
        """
        try:
            # Use specialized builders for main embed types
            if embed_type == 'connection':
                return await cls.build_connection_embed(data)
            elif embed_type == 'killfeed' or embed_type == 'suicide' or embed_type == 'fall':
                return await cls.build_killfeed_embed(data)
            elif embed_type == 'mission':
                return await cls.build_mission_embed(data)
            
            # For other embed types, get themed message
            message_type_map = {
                'airdrop': 'airdrop_incoming',
                'helicrash': 'helicrash_event', 
                'trader': 'trader_arrival'
            }
            
            message_type = message_type_map.get(embed_type)
            if message_type:
                title, description = cls._get_themed_message(message_type)
            else:
                title = data.get('title', 'System Event')
                description = data.get('description', 'Event occurred')
            
            # Get asset info
            asset_filename = cls.ASSETS.get(embed_type, 'main.png')
            asset_path = cls.ASSETS_PATH / asset_filename
            
            # Create file attachment if asset exists
            file_attachment = None
            thumbnail_url = None
            
            if asset_path.exists():
                file_attachment = discord.File(str(asset_path), filename=asset_filename)
                thumbnail_url = f"attachment://{asset_filename}"
            
            # Create base embed
            color = cls.COLORS.get(embed_type, cls.COLORS['info'])
            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )
            
            # Set thumbnail on the right side
            if thumbnail_url:
                embed.set_thumbnail(url=thumbnail_url)
            
            # Add fields based on embed type
            if embed_type == 'airdrop':
                cls._add_airdrop_fields(embed, data)
            elif embed_type == 'helicrash':
                cls._add_helicrash_fields(embed, data)
            elif embed_type == 'trader':
                cls._add_trader_fields(embed, data)
            elif embed_type == 'vehicle':
                cls._add_vehicle_fields(embed, data)
            elif embed_type == 'bounty':
                cls._add_bounty_fields(embed, data)
            elif embed_type == 'economy':
                cls._add_economy_fields(embed, data)
            elif embed_type == 'leaderboard':
                cls._add_leaderboard_fields(embed, data)
            
            # Set footer
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            
            return embed, file_attachment
            
        except Exception as e:
            logger.error(f"Failed to build embed: {e}")
            # Return basic embed as fallback
            fallback_embed = discord.Embed(
                title="System Message",
                description="An error occurred while creating this embed",
                color=cls.COLORS['error'],
                timestamp=datetime.now(timezone.utc)
            )
            fallback_embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return fallback_embed, None

    @classmethod
    def _add_connection_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for connection embeds"""
        player_name = data.get('player_name', 'Unknown Player')
        platform = data.get('platform', 'Unknown')
        server_name = data.get('server_name', 'Unknown Server')
        
        embed.add_field(name="Player", value=player_name, inline=True)
        embed.add_field(name="Platform", value=platform, inline=True)
        embed.add_field(name="Server", value=server_name, inline=True)

    @classmethod
    def _add_mission_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for mission embeds"""
        mission_id = data.get('mission_id', '')
        level = data.get('level', 1)
        state = data.get('state', 'UNKNOWN')
        respawn_time = data.get('respawn_time')
        
        # Normalize mission name
        mission_name = cls.normalize_mission_name(mission_id)
        
        embed.add_field(name="Mission", value=mission_name, inline=False)
        embed.add_field(name="Difficulty Level", value=f"Level {level}", inline=True)
        embed.add_field(name="Status", value=state.replace('_', ' ').title(), inline=True)
        
        if respawn_time:
            embed.add_field(name="Respawn Time", value=f"{respawn_time} seconds", inline=True)

    @classmethod
    def _add_killfeed_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for killfeed embeds"""
        killer = data.get('killer_name', data.get('killer', 'Unknown'))
        victim = data.get('victim_name', data.get('victim', 'Unknown'))
        weapon = data.get('weapon', 'Unknown')
        distance = data.get('distance', '0')
        
        # Convert distance to string for comparison
        distance_str = str(distance)
        
        embed.add_field(name="Killer", value=killer, inline=True)
        embed.add_field(name="Victim", value=victim, inline=True)
        embed.add_field(name="Weapon", value=weapon, inline=True)
        
        # Safe distance comparison - convert to float for numeric check
        try:
            distance_num = float(distance_str)
            if distance_num > 0:
                embed.add_field(name="Distance", value=f"{distance_str}m", inline=True)
        except (ValueError, TypeError):
            pass

    @classmethod
    def _add_suicide_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for suicide embeds"""
        player_name = data.get('player_name', 'Unknown Player')
        cause = data.get('cause', 'Suicide')
        
        embed.add_field(name="Player", value=player_name, inline=True)
        embed.add_field(name="Cause", value=cause, inline=True)

    @classmethod
    def _add_fall_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for fall death embeds"""
        player_name = data.get('player_name', 'Unknown Player')
        
        embed.add_field(name="Player", value=player_name, inline=True)
        embed.add_field(name="Cause", value="Falling Damage", inline=True)

    @classmethod
    def _add_airdrop_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for airdrop embeds"""
        location = data.get('location', 'Unknown Location')
        state = data.get('state', 'incoming')
        
        embed.add_field(name="Location", value=location, inline=True)
        embed.add_field(name="Status", value=state.title(), inline=True)

    @classmethod
    def _add_helicrash_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for helicrash embeds"""
        location = data.get('location', 'Unknown Location')
        
        embed.add_field(name="Crash Site", value=location, inline=True)
        embed.add_field(name="Status", value="Crashed", inline=True)

    @classmethod
    def _add_trader_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for trader embeds"""
        location = data.get('location', 'Unknown Location')
        
        embed.add_field(name="Location", value=location, inline=True)
        embed.add_field(name="Status", value="Available", inline=True)

    @classmethod
    def _add_vehicle_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for vehicle embeds"""
        vehicle_type = data.get('vehicle_type', 'Unknown Vehicle')
        action = data.get('action', 'spawned')
        
        embed.add_field(name="Vehicle", value=vehicle_type, inline=True)
        embed.add_field(name="Action", value=action.title(), inline=True)

    @classmethod
    def _add_bounty_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for bounty embeds"""
        target = data.get('target', 'Unknown')
        amount = data.get('amount', 0)
        poster = data.get('poster', 'Unknown')
        
        embed.add_field(name="Target", value=target, inline=True)
        embed.add_field(name="Bounty", value=f"{amount:,}", inline=True)
        embed.add_field(name="Posted By", value=poster, inline=True)

    @classmethod
    def _add_economy_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for economy embeds"""
        amount = data.get('amount', 0)
        balance = data.get('balance', 0)
        currency = data.get('currency', 'Emeralds')
        
        embed.add_field(name="Amount", value=f"{amount:,} {currency}", inline=True)
        embed.add_field(name="New Balance", value=f"{balance:,} {currency}", inline=True)

    @classmethod
    def _add_leaderboard_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for leaderboard embeds"""
        server_name = data.get('server_name', 'Unknown Server')
        stat_type = data.get('stat_type', 'kills')
        
        embed.add_field(name="Server", value=server_name, inline=True)
        embed.add_field(name="Ranking By", value=stat_type.title(), inline=True)

    @classmethod
    def create_mission_embed(cls, title: str, description: str, mission_id: str, 
                           level: int, state: str, respawn_time: Optional[int] = None) -> discord.Embed:
        """Create a mission embed with proper formatting"""
        try:
            # Get mission color based on level
            if level >= 5:
                color = 0xff0000  # Red for highest level
            elif level >= 4:
                color = 0xff8c00  # Orange for high level
            elif level >= 3:
                color = 0xffd700  # Gold for medium level
            else:
                color = cls.COLORS['mission']  # Default teal for low level
            
            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )
            
            # Add mission details
            mission_name = cls.normalize_mission_name(mission_id)
            embed.add_field(name="Mission", value=mission_name, inline=False)
            embed.add_field(name="Difficulty Level", value=f"Level {level}", inline=True)
            embed.add_field(name="Status", value=state.replace('_', ' ').title(), inline=True)
            
            if respawn_time:
                embed.add_field(name="Respawn Time", value=f"{respawn_time} seconds", inline=True)
            
            # Set thumbnail for mission
            asset_path = cls.ASSETS_PATH / cls.ASSETS['mission']
            if asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{cls.ASSETS['mission']}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed
            
        except Exception as e:
            logger.error(f"Failed to create mission embed: {e}")
            return cls._create_fallback_embed("Mission Update", "Mission status has changed")

    @classmethod
    def create_airdrop_embed(cls, state: str, location: str, timestamp: datetime) -> discord.Embed:
        """Create an airdrop embed"""
        try:
            embed = discord.Embed(
                title="Airdrop Incoming",
                description="Supply drop detected on radar",
                color=cls.COLORS['airdrop'],
                timestamp=timestamp
            )
            
            embed.add_field(name="Location", value=location, inline=True)
            embed.add_field(name="Status", value=state.title(), inline=True)
            
            # Set thumbnail
            asset_path = cls.ASSETS_PATH / cls.ASSETS['airdrop']
            if asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{cls.ASSETS['airdrop']}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed
            
        except Exception as e:
            logger.error(f"Failed to create airdrop embed: {e}")
            return cls._create_fallback_embed("Airdrop", "Supply drop detected")

    @classmethod
    def create_helicrash_embed(cls, location: str, timestamp: datetime) -> discord.Embed:
        """Create a helicrash embed"""
        try:
            embed = discord.Embed(
                title="Helicopter Crash",
                description="Aircraft down, investigate for valuable loot",
                color=cls.COLORS['helicrash'],
                timestamp=timestamp
            )
            
            embed.add_field(name="Crash Site", value=location, inline=True)
            embed.add_field(name="Status", value="Crashed", inline=True)
            
            # Set thumbnail
            asset_path = cls.ASSETS_PATH / cls.ASSETS['helicrash']
            if asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{cls.ASSETS['helicrash']}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed
            
        except Exception as e:
            logger.error(f"Failed to create helicrash embed: {e}")
            return cls._create_fallback_embed("Helicrash", "Helicopter crashed")

    @classmethod
    def create_trader_embed(cls, location: str, timestamp: datetime) -> discord.Embed:
        """Create a trader embed"""
        try:
            embed = discord.Embed(
                title="Trader Arrival",
                description="Black market dealer has arrived",
                color=cls.COLORS['trader'],
                timestamp=timestamp
            )
            
            embed.add_field(name="Location", value=location, inline=True)
            embed.add_field(name="Status", value="Available", inline=True)
            
            # Set thumbnail
            asset_path = cls.ASSETS_PATH / cls.ASSETS['trader']
            if asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{cls.ASSETS['trader']}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed
            
        except Exception as e:
            logger.error(f"Failed to create trader embed: {e}")
            return cls._create_fallback_embed("Trader", "Trader has arrived")

    @classmethod
    def _create_fallback_embed(cls, title: str, description: str) -> discord.Embed:
        """Create a basic fallback embed"""
        return discord.Embed(
            title=title,
            description=description,
            color=cls.COLORS['info'],
            timestamp=datetime.now(timezone.utc)
        )

    @classmethod
    def normalize_mission_name(cls, mission_id: str) -> str:
        """Convert mission ID to readable name"""
        mission_mappings = {
            'GA_Airport_mis_01_SFPSACMission': 'Airport Mission #1',
            'GA_Airport_mis_02_SFPSACMission': 'Airport Mission #2',
            'GA_Airport_mis_03_SFPSACMission': 'Airport Mission #3',
            'GA_Airport_mis_04_SFPSACMission': 'Airport Mission #4',
            'GA_Military_02_Mis1': 'Military Base Mission #2',
            'GA_Military_03_Mis_01': 'Military Base Mission #3',
            'GA_Military_04_Mis1': 'Military Base Mission #4',
            'GA_Beregovoy_Mis1': 'Beregovoy Settlement Mission',
            'GA_Settle_05_ChernyLog_Mis1': 'Cherny Log Settlement Mission',
            'GA_Ind_01_m1': 'Industrial Zone Mission #1',
            'GA_Ind_02_Mis_1': 'Industrial Zone Mission #2',
            'GA_KhimMash_Mis_01': 'Chemical Plant Mission #1',
            'GA_KhimMash_Mis_02': 'Chemical Plant Mission #2',
            'GA_Bunker_01_Mis1': 'Underground Bunker Mission',
            'GA_Sawmill_01_Mis1': 'Sawmill Mission #1',
            'GA_Settle_09_Mis_1': 'Settlement Mission #9',
            'GA_Military_04_Mis_2': 'Military Base Mission #4B',
            'GA_PromZone_6_Mis_1': 'Industrial Zone Mission #6',
            'GA_PromZone_Mis_01': 'Industrial Zone Mission A',
            'GA_PromZone_Mis_02': 'Industrial Zone Mission B',
            'GA_Kamensk_Ind_3_Mis_1': 'Kamensk Industrial Mission',
            'GA_Kamensk_Mis_1': 'Kamensk City Mission #1',
            'GA_Kamensk_Mis_2': 'Kamensk City Mission #2',
            'GA_Kamensk_Mis_3': 'Kamensk City Mission #3',
            'GA_Krasnoe_Mis_1': 'Krasnoe City Mission',
            'GA_Vostok_Mis_1': 'Vostok City Mission',
            'GA_Lighthouse_02_Mis1': 'Lighthouse Mission #2',
            'GA_Elevator_Mis_1': 'Elevator Complex Mission #1',
            'GA_Elevator_Mis_2': 'Elevator Complex Mission #2',
            'GA_Sawmill_02_1_Mis1': 'Sawmill Mission #2A',
            'GA_Sawmill_03_Mis_01': 'Sawmill Mission #3',
            'GA_Bochki_Mis_1': 'Barrel Storage Mission',
            'GA_Dubovoe_0_Mis_1': 'Dubovoe Resource Mission',
        }
        
        return mission_mappings.get(mission_id, mission_id.replace('_', ' ').title())

    @classmethod
    def get_mission_level(cls, mission_id: str) -> int:
        """Determine mission difficulty level"""
        # High-tier missions (level 5)
        high_tier = [
            'GA_Airport_mis_04_SFPSACMission',
            'GA_Military_04_Mis1',
            'GA_Military_04_Mis_2',
            'GA_Bunker_01_Mis1',
            'GA_KhimMash_Mis_02'
        ]
        
        # Medium-high tier missions (level 4)
        medium_high_tier = [
            'GA_Airport_mis_03_SFPSACMission',
            'GA_Military_03_Mis_01',
            'GA_KhimMash_Mis_01',
            'GA_Kamensk_Mis_3',
            'GA_Elevator_Mis_2'
        ]
        
        # Medium tier missions (level 3)
        medium_tier = [
            'GA_Airport_mis_02_SFPSACMission',
            'GA_Military_02_Mis1',
            'GA_Ind_02_Mis_1',
            'GA_Kamensk_Mis_1',
            'GA_Kamensk_Mis_2',
            'GA_Krasnoe_Mis_1',
            'GA_Vostok_Mis_1',
            'GA_Elevator_Mis_1',
            'GA_Sawmill_03_Mis_01'
        ]
        
        if mission_id in high_tier:
            return 5
        elif mission_id in medium_high_tier:
            return 4
        elif mission_id in medium_tier:
            return 3
        else:
            return 2  # Low tier missions
