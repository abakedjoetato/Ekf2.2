
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

    # Random atmospheric messages for killfeed embeds
    KILLFEED_ATMOSPHERIC_MESSAGES = {
        'kill': [
            "> Another heartbeat silenced beneath the ash sky.",
            "> No burial, no name — just silence where a soul once stood.",
            "> Left no echo. Just scattered gear and cooling blood.",
            "> Cut from the world like thread from a fraying coat.",
            "> Hunger, cold, bullets — it could've been any of them. It was enough.",
            "> Marked, hunted, forgotten. In that order.",
            "> Their fire went out before they even knew they were burning.",
            "> A last breath swallowed by wind and war.",
            "> The price of survival paid in someone else's blood.",
            "> The map didn't change. The player did."
        ],
        'suicide': [
            "> Hit \"relocate\" like it was the snooze button. Got deleted.",
            "> Tactical redeployment... into the abyss.",
            "> Rage respawned and logic respawned with it.",
            "> Wanted a reset. Got a reboot straight to the void.",
            "> Pressed something. Paid everything.",
            "> Who needs enemies when you've got bad decisions?",
            "> Alt+F4'd themselves into Valhalla.",
            "> Strategic death — poorly executed.",
            "> Fast travel without a destination.",
            "> Confirmed: the dead menu is not a safe zone."
        ],
        'fall': [
            "> Thought they could make it. The ground disagreed.",
            "> Airborne ambition. Terminal results.",
            "> Tried flying. Landed poorly.",
            "> Gravity called. They answered — headfirst.",
            "> Believed in themselves. Gravity didn't.",
            "> From rooftops to regret in under two seconds.",
            "> The sky opened. The floor closed.",
            "> Survival instincts took a coffee break.",
            "> Feet first into a bad decision.",
            "> Their plan had one fatal step too many."
        ]
    }

    # Themed messages for each embed type - EXPANDED POOLS
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
            ("Fresh Blood Arrives", "New combatant has entered the warzone"),
            ("Unit Deployed", "New tactical asset has entered the field"),
            ("Ally Reinforcement", "Additional friendly forces have arrived"),
            ("Combat Ready", "New operative is mission-ready and armed"),
            ("Field Agent Active", "Special forces unit now operational"),
            ("Strike Team Member", "Elite operator has joined the battlefield"),
            ("Tactical Insert", "Specialist unit deployed to combat zone"),
            ("Boots on Ground", "Infantry unit has entered the operational area"),
            ("Mission Support", "Additional resources now available"),
            ("Operative Online", "Field agent reporting for active duty"),
            ("Battle Ready", "New combatant prepared for engagement")
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
            ("Fade to Black", "Last transmission received from departing unit"),
            ("Stand Down", "Operative has been relieved from active duty"),
            ("Exfiltration Success", "Agent successfully extracted from the field"),
            ("Mission Wrap", "Operational tour has reached completion"),
            ("Signal Lost", "Connection terminated with field operative"),
            ("RTB Confirmed", "Return to base mission accomplished"),
            ("Off Duty", "Operator has concluded combat operations"),
            ("Ghost Protocol", "Agent has vanished from the battlefield"),
            ("Mission End", "Tactical assignment successfully completed"),
            ("Withdrawal Complete", "Strategic pullback executed flawlessly"),
            ("Final Transmission", "Last communication received from operative")
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
            ("Threat Eliminated", "The wasteland's brutal law prevails"),
            ("Fatal Encounter", "Another casualty of the contaminated world"),
            ("Engagement Resolved", "Superior firepower claims another victim"),
            ("Combat Casualty", "The harsh reality of survival warfare"),
            ("Tactical Victory", "Strategic elimination successfully executed"),
            ("Hostile Terminated", "Enemy combatant permanently neutralized"),
            ("Lethal Force Applied", "Deadly encounter resolved decisively"),
            ("Target Acquired", "Precision strike eliminates hostile threat"),
            ("Enemy Neutralized", "Opposition force permanently disabled"),
            ("Combat Effective", "Deadly engagement concluded successfully"),
            ("Elimination Successful", "Hostile target removed from battlefield")
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
            ("Self-Destruct Sequence", "Someone skipped the safety briefing"),
            ("Operator Error", "RTFM should have been mandatory reading"),
            ("Epic Fail", "Achievement unlocked: Ultimate facepalm"),
            ("Darwin Award", "Natural selection working as intended"),
            ("Auto-Delete", "Self-removal protocol activated successfully"),
            ("Friendly Fire", "Plot twist: the call was coming from inside"),
            ("System Crash", "Blue screen of death, literally"),
            ("User Input Error", "Keyboard error: Press F to pay respects"),
            ("Accidental Activation", "Read the instructions, they said"),
            ("Critical Failure", "Murphy's Law strikes again"),
            ("Self-Termination", "Took 'going out with a bang' literally")
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
            ("Elevation Miscalculation", "Overestimated their frequent flyer miles"),
            ("Vertical Velocity Error", "Speed limit exceeded in the downward direction"),
            ("Parachute Malfunction", "Backup chute was also out of order"),
            ("Aerodynamic Failure", "Turns out humans are terrible at flying"),
            ("Ground Proximity Alert", "Warning came a little too late"),
            ("Emergency Landing", "Forgot to request clearance from the ground"),
            ("Atmospheric Re-entry", "Came in too hot without heat shields"),
            ("Cliff Notes", "Took a shortcut that went straight down"),
            ("Diving Accident", "Olympic scoring: Perfect 10 for form"),
            ("Flight Training", "Lesson one: Landing is usually optional"),
            ("Altitude Sickness", "Cure was found at ground level")
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
            ("Battle Orders", "Tactical engagement zone is active"),
            ("Assignment Ready", "High-priority operation awaiting execution"),
            ("Mission Package", "Strategic directive now available for action"),
            ("Objective Briefing", "Critical mission zone has been activated"),
            ("Tactical Deployment", "Elite operation ready for specialized units"),
            ("Priority Target", "High-value objective now accessible"),
            ("Operation Alert", "Strategic mission parameters established"),
            ("Mission Protocol", "Tactical engagement zone now operational"),
            ("Directive Active", "Combat mission ready for deployment"),
            ("Strategic Objective", "Priority operation cleared for execution"),
            ("Combat Assignment", "Tactical mission zone now available"),
            ("Field Operation", "Specialized mission ready for elite forces"),
            ("Tactical Brief", "Strategic operation parameters confirmed"),
            ("Mission Clearance", "High-priority objective zone activated"),
            ("Operation Status", "Critical mission deployment authorized"),
            ("Assignment Brief", "Tactical operation ready for execution")
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
            ("Air Logistics", "Supply package incoming from above"),
            ("Cargo Flight", "Aerial supply mission on final vector"),
            ("Drop Zone Active", "Supply aircraft approaching designated area"),
            ("Supply Vector", "Logistics delivery confirmed inbound"),
            ("Aerial Package", "High-altitude cargo drop in progress"),
            ("Sky Cargo", "Supply aircraft on delivery approach"),
            ("Logistics Drop", "Aerial resupply package incoming"),
            ("Supply Mission", "Cargo aircraft confirmed on approach"),
            ("Drop Incoming", "Aerial delivery system activated"),
            ("Cargo Delivery", "Supply drop mission in final approach"),
            ("Air Supply", "Logistics aircraft inbound with cargo")
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
            ("Rotor Failure", "Helicopter suffered mechanical failure"),
            ("Forced Landing", "Rotorcraft emergency descent completed"),
            ("Aviation Emergency", "Helicopter distress situation confirmed"),
            ("Crash Landing", "Aircraft emergency touchdown reported"),
            ("Wreckage Detected", "Helicopter debris field located"),
            ("Emergency Beacon", "Aircraft distress signal activated"),
            ("Mayday Situation", "Helicopter emergency landing confirmed"),
            ("Flight Incident", "Rotorcraft operational failure reported"),
            ("Aircraft Emergency", "Helicopter forced landing executed"),
            ("Crash Zone", "Aviation incident site now active"),
            ("Emergency Touchdown", "Helicopter distress landing completed")
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
            ("Underworld Trading", "Shadow market is now operational"),
            ("Commerce Active", "Independent trader open for business"),
            ("Vendor Available", "Specialized merchant now accessible"),
            ("Trade Post Open", "Commercial vendor ready for transactions"),
            ("Market Vendor", "Underground trader conducting sales"),
            ("Dealer Network", "Black market contact now available"),
            ("Commerce Hub", "Trading post now operational"),
            ("Merchant Contact", "Underground dealer ready for business"),
            ("Trade Terminal", "Commercial vendor now accessible"),
            ("Supply Contact", "Independent trader open for deals"),
            ("Exchange Active", "Underground market now operational")
        ],
        'vehicle_spawn': [
            ("Vehicle Deployed", "New transportation asset now available"),
            ("Motor Pool Active", "Vehicle has been deployed to the field"),
            ("Transport Ready", "New vehicle asset operational"),
            ("Wheels Up", "Transportation unit now available"),
            ("Vehicle Online", "Mobile asset deployed and ready"),
            ("Transport Arrival", "New vehicle has entered the battlefield"),
            ("Motor Asset", "Transportation resource now operational"),
            ("Vehicle Ready", "Mobile unit deployed for field use"),
            ("Transport Active", "New vehicle asset available"),
            ("Mobile Unit", "Transportation deployed to combat zone")
        ],
        'vehicle_delete': [
            ("Vehicle Lost", "Transportation asset no longer operational"),
            ("Transport Down", "Vehicle has been removed from service"),
            ("Motor Pool Loss", "Vehicle asset no longer available"),
            ("Wheels Down", "Transportation unit out of commission"),
            ("Vehicle Offline", "Mobile asset removed from operation"),
            ("Transport Removed", "Vehicle no longer battlefield ready"),
            ("Motor Loss", "Transportation resource unavailable"),
            ("Vehicle Destroyed", "Mobile unit eliminated from service"),
            ("Transport Inactive", "Vehicle asset removed from field"),
            ("Mobile Down", "Transportation no longer operational")
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
            
            # Set thumbnail with case-insensitive lookup
            asset_path, asset_filename = cls._get_asset_path('connection')
            file_attachment = None
            if asset_path and asset_path.exists():
                file_attachment = discord.File(str(asset_path), filename=asset_filename)
                embed.set_thumbnail(url=f"attachment://{asset_filename}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed, file_attachment
            
        except Exception as e:
            logger.error(f"Failed to build connection embed: {e}")
            return cls._create_fallback_embed("Connection Event", "Player activity recorded")

    @classmethod
    async def build_killfeed_embed(cls, data: Dict[str, Any]) -> Tuple[discord.Embed, Optional[discord.File]]:
        """Build themed killfeed embed"""
        try:
            import random
            
            is_suicide = data.get('is_suicide', False)
            weapon = data.get('weapon', 'Unknown')
            
            # Determine message type and atmospheric message type
            if is_suicide:
                if 'fall' in weapon.lower() or 'falling' in weapon.lower():
                    message_type = 'killfeed_fall'
                    atmospheric_type = 'fall'
                else:
                    message_type = 'killfeed_suicide'
                    atmospheric_type = 'suicide'
            else:
                message_type = 'killfeed_kill'
                atmospheric_type = 'kill'
            
            # Get themed message (use title only)
            title, _ = cls._get_themed_message(message_type)
            
            # Get random atmospheric message
            atmospheric_messages = cls.KILLFEED_ATMOSPHERIC_MESSAGES.get(atmospheric_type, [])
            atmospheric_message = random.choice(atmospheric_messages) if atmospheric_messages else ""
            
            # Create embed with appropriate color based on death type
            if is_suicide:
                if 'fall' in weapon.lower() or 'falling' in weapon.lower():
                    color = 0xa855f7  # Purple for falling deaths
                else:
                    color = 0xff0000  # Red for suicide
            else:
                color = 0xffd700  # Gold for kills
            embed = discord.Embed(
                title=title,
                description=atmospheric_message,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )
            
            if is_suicide:
                # Suicide embed
                player_name = data.get('victim', data.get('player_name', 'Unknown'))
                embed.add_field(name="Player", value=player_name, inline=True)
                embed.add_field(name="Cause", value=weapon, inline=True)
                
                # Use appropriate asset key
                asset_key = 'falling' if 'fall' in weapon.lower() else 'suicide'
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
                    
                asset_key = 'killfeed'
            
            # Set thumbnail with case-insensitive lookup
            asset_path, asset_filename = cls._get_asset_path(asset_key)
            file_attachment = None
            if asset_path and asset_path.exists():
                file_attachment = discord.File(str(asset_path), filename=asset_filename)
                embed.set_thumbnail(url=f"attachment://{asset_filename}")
            
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
            
            # Set thumbnail with case-insensitive lookup
            asset_path, asset_filename = cls._get_asset_path('mission')
            file_attachment = None
            if asset_path and asset_path.exists():
                file_attachment = discord.File(str(asset_path), filename=asset_filename)
                embed.set_thumbnail(url=f"attachment://{asset_filename}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed, file_attachment
            
        except Exception as e:
            logger.error(f"Failed to build mission embed: {e}")
            return cls._create_fallback_embed("Mission Update", "Mission status changed")

    @classmethod
    def _get_asset_path(cls, asset_key: str) -> Tuple[Optional[Path], Optional[str]]:
        """
        Get asset path with case-insensitive fallback
        Returns (asset_path, filename) tuple
        """
        # Get the expected filename for this asset key
        asset_filename = cls.ASSETS.get(asset_key, 'main.png')
        asset_path = cls.ASSETS_PATH / asset_filename
        
        # Try exact match first
        if asset_path.exists():
            return asset_path, asset_filename
        
        # If exact match fails, try case-insensitive search
        if cls.ASSETS_PATH.exists():
            try:
                target_filename_lower = asset_filename.lower()
                for file_path in cls.ASSETS_PATH.iterdir():
                    if file_path.is_file() and file_path.name.lower() == target_filename_lower:
                        logger.info(f"✅ Found case-insensitive match: {file_path.name} for {asset_filename}")
                        return file_path, file_path.name
                
                # If still not found, try partial matching for common variations
                base_name = asset_filename.lower().replace('.png', '')
                for file_path in cls.ASSETS_PATH.iterdir():
                    if file_path.is_file():
                        file_name_lower = file_path.name.lower()
                        if base_name in file_name_lower and file_name_lower.endswith('.png'):
                            logger.info(f"✅ Found partial match: {file_path.name} for {asset_filename}")
                            return file_path, file_path.name
                            
            except Exception as e:
                logger.warning(f"Error during case-insensitive asset search: {e}")
        
        # Return fallback to main.png if nothing found
        fallback_path = cls.ASSETS_PATH / 'main.png'
        if fallback_path.exists():
            logger.warning(f"Using fallback asset main.png for missing {asset_filename}")
            return fallback_path, 'main.png'
        
        # Return None if even fallback doesn't exist
        logger.error(f"No asset found for {asset_key}, fallback main.png also missing")
        return None, None

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
            
            # Get asset info with case-insensitive lookup
            asset_path, asset_filename = cls._get_asset_path(embed_type)
            
            # Create file attachment if asset exists
            file_attachment = None
            thumbnail_url = None
            
            if asset_path and asset_path.exists():
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
            
            # Set thumbnail for mission with case-insensitive lookup
            asset_path, asset_filename = cls._get_asset_path('mission')
            if asset_path and asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{asset_filename}")
            
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
            
            # Set thumbnail with case-insensitive lookup
            asset_path, asset_filename = cls._get_asset_path('airdrop')
            if asset_path and asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{asset_filename}")
            
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
            
            # Set thumbnail with case-insensitive lookup
            asset_path, asset_filename = cls._get_asset_path('helicrash')
            if asset_path and asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{asset_filename}")
            
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
            
            # Set thumbnail with case-insensitive lookup
            asset_path, asset_filename = cls._get_asset_path('trader')
            if asset_path and asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{asset_filename}")
            
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
