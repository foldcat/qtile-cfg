from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import subprocess

mod = "mod4"
terminal = "alacritty"

@hook.subscribe.startup_once
def autostart_once():
    if qtile.core.name == "x11":
        subprocess.run(["xset", "r", "rate", "300", "25"])
        subprocess.run(["xset", "s", "off"])
        subprocess.run(["xset", "s", "noblank"])
        subprocess.run(["xset", "-dpms"])
    subprocess.run(["dbus-update-activation-environment", "DISPLAY"])
    subprocess.Popen(["/usr/libexec/polkit-gnome-authentication-agent-1"])
    subprocess.Popen(["dunst"])

keys = [
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    Key([mod], "l", lazy.layout.grow_main(), desc="Grow main"),
    Key([mod], "h", lazy.layout.shrink_main(), desc="Shrink Main"),
    Key([mod, "shift"], "h", lazy.layout.grow(), desc="Grow window"),
    Key([mod, "shift"], "l", lazy.layout.shrink(), desc="Shrink window"),

    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),

    Key([mod], "Return", lazy.layout.swap_main(), desc="Move window to master"),

    Key([mod, "shift"], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "p", lazy.spawn("j4-dmenu-desktop"), desc="Spawn Launcher"),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([], "f9", lazy.spawn("flameshot gui"), desc="Take Screenshot"),

    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume -l 1.5 @DEFAULT_AUDIO_SINK@ 5%-"), desc="Lower Volume by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume -l 1.5 @DEFAULT_AUDIO_SINK@ 5%+"), desc="Raise Volume by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"), desc="Mute/Unmute Volume"),

    Key([], "Print", lazy.spawn("flameshot gui"), desc="Screenshot"),
    Key([], "f9", lazy.spawn("flameshot gui"), desc="Screenshot"),
]

for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
        ]
    )

layouts = [
    layout.MonadTall(new_client_position="bottom", border_focus=["#33b1ff"]),
    layout.Max(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font Mono",
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

widgets = [
    widget.GroupBox(this_current_screen_border="#33b1ff"),
    widget.TextBox(fmt="|", foreground="404040"),
    widget.CurrentLayout(foreground="808080"),
    widget.TextBox(fmt="|", foreground="404040"),
    widget.Prompt(),
    widget.WindowName(),
    widget.Chord(
        chords_colors={
            "launch": ("#ff0000", "#ffffff"),
        },
        name_transform=lambda name: name.upper(),
    ),
    widget.Net(format="[NET {down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}]"),
    widget.PulseVolume(unmute_format="[VOL {volume}%]", mute_format="[VOL MUTE]"),
    widget.CPU(format="[CPU {load_percent}%]"),
    widget.Memory(format="[MEM {MemPercent}%]"),
    widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
]

if qtile.core.name == "x11":
    widgets.append(widget.Systray())
elif qtile.core.name == "wayland":
    widgets.append(widget.StatusNotifier())

screens = [
    Screen(
        bottom=bar.Bar(
            widgets,
      24,
        ),
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.toggle_floating()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus="#ff7eb6",
    border_width=2,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True

wl_input_rules = None

wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "maidwm"
