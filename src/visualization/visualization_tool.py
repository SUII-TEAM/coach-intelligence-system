import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from langchain.tools import Tool
import numpy as np
import io
import base64


class VisualizationTool:
    def __init__(self):
        self.name = "visualization_tool"
        self.description = """
        Use this tool to generate visual representations of football data, formations, and strategies.
        This is useful for creating formation diagrams, heat maps, and other visual aids.
        """

        # Create the tool
        self.tool = Tool.from_function(
            func=self.visualize,
            name=self.name,
            description=self.description
        )

        # Create directory for saving visualizations
        os.makedirs("src/visualization/output", exist_ok=True)
        self.output_dir = "src/visualization/output"

    def visualize(self, data, visualization_type="formation", title=None, save_path=None):
        """
        Generate visualizations based on the provided data

        Args:
            data: Data to visualize (formations, statistics, etc.)
            visualization_type (str): Type of visualization (formation, stats, etc.)
            title (str, optional): Title for the visualization
            save_path (str, optional): Path to save the visualization

        Returns:
            str: Description of the visualization and/or path to the saved image
        """
        try:
            if visualization_type.lower() == "formation":
                return self._visualize_formation(data, title, save_path)
            elif visualization_type.lower() == "stats":
                return self._visualize_stats(data, title, save_path)
            elif visualization_type.lower() == "match_events":
                return self._visualize_match_events(data, title, save_path)
            else:
                return f"Unsupported visualization type: {visualization_type}"

        except Exception as e:
            return f"Error generating visualization: {str(e)}"

    def _visualize_formation(self, formation_data, title=None, save_path=None):
        """Create a football formation diagram"""
        # Parse formation data if it's a string
        if isinstance(formation_data, str):
            try:
                if "{" in formation_data:  # Looks like JSON
                    formation_data = json.loads(formation_data)
                else:  # Simple formation string like "4-4-2"
                    formation_data = {"formation": formation_data}
            except:
                formation_data = {"formation": formation_data}

        # Extract formation info
        formation = formation_data.get("formation", "4-4-2")

        # Create a blank football pitch
        fig, ax = plt.subplots(figsize=(10, 7))

        # Draw the pitch
        self._draw_pitch(ax)

        # Place players based on formation
        self._place_players(ax, formation)

        # Set the title
        if title:
            plt.title(title, fontsize=16)
        else:
            plt.title(f"Formation: {formation}", fontsize=16)

        # Remove axes
        plt.axis('off')

        # Save or show the visualization
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return f"Formation visualization saved to {save_path}"
        else:
            # Generate a default filename
            filename = f"{formation.replace('-', '_')}_formation.png"
            full_path = os.path.join(self.output_dir, filename)
            plt.savefig(full_path, dpi=300, bbox_inches='tight')
            plt.close()

            # For prototype purposes, return the path to the saved image
            # In a real implementation, this might return a web URL or encoded image
            return f"Formation visualization created:\n{full_path}"

    def _draw_pitch(self, ax):
        """Draw a football pitch"""
        # Pitch dimensions
        pitch_length = 105
        pitch_width = 68

        # Draw pitch outline
        rect = patches.Rectangle((0, 0), pitch_length, pitch_width, linewidth=2,
                                 edgecolor='white', facecolor='#3A9648')
        ax.add_patch(rect)

        # Draw halfway line
        plt.plot([pitch_length/2, pitch_length/2], [0, pitch_width], 'white')

        # Draw center circle
        center_circle = plt.Circle(
            (pitch_length/2, pitch_width/2), 9.15, fill=False, color='white')
        ax.add_patch(center_circle)

        # Draw center spot
        center_spot = plt.Circle(
            (pitch_length/2, pitch_width/2), 0.8, color='white')
        ax.add_patch(center_spot)

        # Draw penalty areas
        # Left penalty area
        left_pen = patches.Rectangle((0, pitch_width/2 - 20.16), 16.5, 40.32,
                                     linewidth=2, edgecolor='white', facecolor='none')
        ax.add_patch(left_pen)

        # Right penalty area
        right_pen = patches.Rectangle((pitch_length - 16.5, pitch_width/2 - 20.16), 16.5, 40.32,
                                      linewidth=2, edgecolor='white', facecolor='none')
        ax.add_patch(right_pen)

        # Draw goal areas
        # Left goal area
        left_goal = patches.Rectangle((0, pitch_width/2 - 9.16), 5.5, 18.32,
                                      linewidth=2, edgecolor='white', facecolor='none')
        ax.add_patch(left_goal)

        # Right goal area
        right_goal = patches.Rectangle((pitch_length - 5.5, pitch_width/2 - 9.16), 5.5, 18.32,
                                       linewidth=2, edgecolor='white', facecolor='none')
        ax.add_patch(right_goal)

        # Draw penalty spots
        left_pen_spot = plt.Circle((11, pitch_width/2), 0.8, color='white')
        ax.add_patch(left_pen_spot)

        right_pen_spot = plt.Circle(
            (pitch_length - 11, pitch_width/2), 0.8, color='white')
        ax.add_patch(right_pen_spot)

        # Set axis limits
        ax.set_xlim(-5, pitch_length + 5)
        ax.set_ylim(-5, pitch_width + 5)

    def _place_players(self, ax, formation):
        """Place players on the pitch according to the formation"""
        # Parse formation string (e.g., "4-4-2", "4-3-3", etc.)
        try:
            # Handle formations with up to 5 lines (e.g., 3-4-2-1)
            formation_parts = formation.split("-")
            # Ensure we have at least 4 parts (defense, mid, attack)
            while len(formation_parts) < 4:
                formation_parts.append("0")

            # Extract the numbers for each line
            defense_num = int(formation_parts[0])
            mid_num = int(formation_parts[1])

            # For formations like 4-2-3-1, combine the additional midfield layers
            if len(formation_parts) > 3:
                attacking_mid_num = int(formation_parts[2])
                forwards_num = int(formation_parts[3])
            else:
                attacking_mid_num = 0
                forwards_num = int(formation_parts[2])

            # Pitch dimensions
            pitch_length = 105
            pitch_width = 68

            # Team will attack from left to right

            # Place goalkeeper
            gk_x = 5
            gk_y = pitch_width / 2
            self._draw_player(ax, gk_x, gk_y, "GK", "red")

            # Place defenders
            if defense_num > 0:
                def_y_positions = np.linspace(
                    10, pitch_width - 10, defense_num)
                def_x = 20
                for i, y_pos in enumerate(def_y_positions):
                    self._draw_player(ax, def_x, y_pos, f"D{i+1}", "blue")

            # Place midfielders
            if mid_num > 0:
                mid_y_positions = np.linspace(10, pitch_width - 10, mid_num)
                mid_x = 40
                for i, y_pos in enumerate(mid_y_positions):
                    self._draw_player(ax, mid_x, y_pos, f"M{i+1}", "green")

            # Place attacking midfielders if present
            if attacking_mid_num > 0:
                att_mid_y_positions = np.linspace(
                    15, pitch_width - 15, attacking_mid_num)
                att_mid_x = 60
                for i, y_pos in enumerate(att_mid_y_positions):
                    self._draw_player(ax, att_mid_x, y_pos,
                                      f"AM{i+1}", "purple")

            # Place forwards
            if forwards_num > 0:
                fw_y_positions = np.linspace(
                    20, pitch_width - 20, forwards_num)
                fw_x = 80
                for i, y_pos in enumerate(fw_y_positions):
                    self._draw_player(ax, fw_x, y_pos, f"F{i+1}", "orange")

        except Exception as e:
            # If there's an error parsing, default to 4-4-2
            ax.text(pitch_length/2, pitch_width + 5, f"Error parsing formation '{formation}': {str(e)}",
                    ha='center', color='red')

            # Default to a simple 4-4-2
            # Defenders
            def_y_positions = np.linspace(10, pitch_width - 10, 4)
            def_x = 20
            for i, y_pos in enumerate(def_y_positions):
                self._draw_player(ax, def_x, y_pos, f"D{i+1}", "blue")

            # Midfielders
            mid_y_positions = np.linspace(10, pitch_width - 10, 4)
            mid_x = 50
            for i, y_pos in enumerate(mid_y_positions):
                self._draw_player(ax, mid_x, y_pos, f"M{i+1}", "green")

            # Forwards
            fw_y_positions = np.linspace(pitch_width/3, 2*pitch_width/3, 2)
            fw_x = 80
            for i, y_pos in enumerate(fw_y_positions):
                self._draw_player(ax, fw_x, y_pos, f"F{i+1}", "orange")

    def _draw_player(self, ax, x, y, label, color):
        """Draw a player on the pitch"""
        player = plt.Circle((x, y), 2.5, color=color)
        ax.add_patch(player)
        ax.text(x, y, label, ha='center', va='center',
                color='white', fontweight='bold')

    def _visualize_stats(self, stats_data, title=None, save_path=None):
        """Create a visualization of match statistics"""
        # Parse stats data if it's a string
        if isinstance(stats_data, str):
            try:
                stats_data = json.loads(stats_data)
            except:
                return "Error: Stats data must be a valid JSON string"

        # Extract team names and stats
        home_team = stats_data.get("home_team", {}).get("name", "Home Team")
        away_team = stats_data.get("away_team", {}).get("name", "Away Team")

        # Get stats to compare
        stats_to_compare = {
            "Possession (%)": [
                stats_data.get("home_team", {}).get("possession", 50),
                stats_data.get("away_team", {}).get("possession", 50)
            ],
            "Shots on Target": [
                stats_data.get("home_team", {}).get("shots_on_target", 0),
                stats_data.get("away_team", {}).get("shots_on_target", 0)
            ],
            "Corners": [
                stats_data.get("home_team", {}).get("corners", 0),
                stats_data.get("away_team", {}).get("corners", 0)
            ],
            "Yellow Cards": [
                stats_data.get("home_team", {}).get(
                    "cards", {}).get("yellow", 0),
                stats_data.get("away_team", {}).get(
                    "cards", {}).get("yellow", 0)
            ]
        }

        # Create the figure
        fig, axes = plt.subplots(
            len(stats_to_compare), 1, figsize=(10, 3 * len(stats_to_compare)))

        # Make axes iterable even if there's only one stat
        if len(stats_to_compare) == 1:
            axes = [axes]

        # Plot each stat as a horizontal bar
        for i, (stat_name, values) in enumerate(stats_to_compare.items()):
            ax = axes[i]

            # For possession, show as a single bar with two colors
            if stat_name == "Possession (%)":
                ax.barh([0], [values[0]], color='blue', label=home_team)
                ax.barh([0], [values[1]], left=[values[0]],
                        color='red', label=away_team)

                # Add text in the middle of each part of the bar
                ax.text(values[0]/2, 0, f"{values[0]}%", va='center',
                        ha='center', color='white', fontweight='bold')
                ax.text(values[0] + values[1]/2, 0, f"{values[1]}%",
                        va='center', ha='center', color='white', fontweight='bold')

                # Remove y-ticks
                ax.set_yticks([])
            else:
                # For other stats, show as side-by-side bars
                x = np.arange(1)
                width = 0.35

                ax.barh([0], [values[0]], height=width,
                        color='blue', label=home_team)
                ax.barh([0 + width], [values[1]], height=width,
                        color='red', label=away_team)

                # Add value labels to the bars
                ax.text(values[0] + 0.1, 0, str(values[0]), va='center')
                ax.text(values[1] + 0.1, 0 + width,
                        str(values[1]), va='center')

                # Set y-tick labels
                ax.set_yticks([0, width])
                ax.set_yticklabels([home_team, away_team])

            # Set title for the subplot
            ax.set_title(stat_name)

            # Only show legend for the first subplot
            if i == 0:
                ax.legend()

            # Remove x-label and grid for cleaner look
            ax.set_xlabel('')
            ax.grid(False)

            # Increase font size
            ax.tick_params(axis='both', which='major', labelsize=12)
            ax.title.set_fontsize(14)

        # Set overall title
        if title:
            fig.suptitle(title, fontsize=16)
        else:
            fig.suptitle(
                f"Match Statistics: {home_team} vs {away_team}", fontsize=16)

        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)

        # Save or show the visualization
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return f"Statistics visualization saved to {save_path}"
        else:
            # Generate a default filename
            filename = f"{home_team}_vs_{away_team}_stats.png"
            # Remove spaces and special characters
            filename = filename.replace(" ", "_").replace("/", "_")
            full_path = os.path.join(self.output_dir, filename)
            plt.savefig(full_path, dpi=300, bbox_inches='tight')
            plt.close()

            return f"Statistics visualization created:\n{full_path}"

    def _visualize_match_events(self, events_data, title=None, save_path=None):
        """Create a visualization of match events (goals, cards, etc.)"""
        # Parse events data if it's a string
        if isinstance(events_data, str):
            try:
                events_data = json.loads(events_data)
            except:
                return "Error: Events data must be a valid JSON string"

        # Extract match information
        match_id = events_data.get("match_id", "Unknown Match")
        home_team = events_data.get("home_team", {}).get("name", "Home Team")
        away_team = events_data.get("away_team", {}).get("name", "Away Team")
        current_minute = events_data.get("minute", 90)

        # Extract events
        events = events_data.get("events", [])

        # Create the figure
        fig, ax = plt.subplots(figsize=(12, 6))

        # Draw a timeline
        ax.axhline(y=1, xmin=0, xmax=90, color='gray',
                   linestyle='-', alpha=0.5)

        # Mark current minute
        ax.axvline(x=current_minute, color='red', linestyle='--',
                   label=f"Current Minute: {current_minute}")

        # Dictionary to hold event icons and colors
        event_props = {
            "goal": {"marker": "o", "color": "green", "size": 150, "label": "Goal"},
            "yellow_card": {"marker": "s", "color": "yellow", "size": 100, "label": "Yellow Card"},
            "red_card": {"marker": "s", "color": "red", "size": 100, "label": "Red Card"},
            "substitution": {"marker": "^", "color": "blue", "size": 100, "label": "Substitution"},
            "penalty": {"marker": "P", "color": "purple", "size": 150, "label": "Penalty"}
        }

        # Track which event types have been added to legend
        legend_added = set()

        # Plot each event
        for event in events:
            minute = event.get("minute", 0)
            event_type = event.get("type", "").lower()
            team = event.get("team", "")
            player = event.get("player", "")

            # Determine y-position based on team
            y_pos = 1.1 if team == home_team else 0.9

            # Get event properties
            props = event_props.get(
                event_type, {"marker": "o", "color": "gray", "size": 100, "label": "Other"})

            # Add to legend only if not already added
            label = props["label"] if event_type not in legend_added else None
            if label:
                legend_added.add(event_type)

            # Plot the event
            ax.scatter(minute, y_pos, marker=props["marker"], color=props["color"],
                       s=props["size"], label=label, edgecolor='black', linewidth=1)

            # Add text label for the event
            if event_type == "goal":
                text = f"{player} ⚽"
            elif event_type == "yellow_card":
                text = f"{player} 🟨"
            elif event_type == "red_card":
                text = f"{player} 🟥"
            elif event_type == "substitution":
                text = f"{player} ↺"
            else:
                text = player

            rotation = 45 if team == home_team else -45
            y_offset = 0.05 if team == home_team else -0.05

            ax.text(minute, y_pos + y_offset, text, rotation=rotation,
                    ha='center', va='center' if team == home_team else 'top',
                    fontsize=9, fontweight='bold')

        # Set axis limits
        ax.set_xlim(0, 90)
        ax.set_ylim(0.7, 1.3)

        # Set y-axis labels for teams
        ax.set_yticks([0.9, 1.1])
        ax.set_yticklabels([away_team, home_team])

        # Add x-axis ticks for minutes
        ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
        ax.set_xticklabels(
            ['0\'', '15\'', '30\'', '45\'', '60\'', '75\'', '90\''])

        # Add title
        if title:
            plt.title(title, fontsize=16)
        else:
            plt.title(f"Match Events: {home_team} vs {away_team}", fontsize=16)

        # Add legend
        plt.legend(loc='upper center', bbox_to_anchor=(
            0.5, -0.05), ncol=len(legend_added) + 1)

        # Save or show the visualization
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return f"Match events visualization saved to {save_path}"
        else:
            # Generate a default filename
            filename = f"{home_team}_vs_{away_team}_events.png"
            # Remove spaces and special characters
            filename = filename.replace(" ", "_").replace("/", "_")
            full_path = os.path.join(self.output_dir, filename)
            plt.savefig(full_path, dpi=300, bbox_inches='tight')
            plt.close()

            return f"Match events visualization created:\n{full_path}"
