from worlds.LauncherComponents import Component, Type, components, launch

from .world import BG3World as BG3World


# Apart from the regular apworld code that allows generating multiworld seeds with your game,
# your apworld might have other "components" that should be launchable from the Archipelago Launcher.
# The most common type of component is a client, but there are other components, such as sprite/palette adjusters.
# (Note: Some worlds distribute their clients as separate, standalone programs,
#  while others include them in the apworld itself. Standalone clients are not an apworld component,
#  although you could make a component that e.g. auto-installs and launches the standalone client for the user.)
# APQuest has a Python client inside the apworld that contains the entire game. This is a component.
# APQuest will not teach you how to make a client or any other type of component.
# However, let's quickly talk about how you register a component to be launchable from the Archipelago Launcher.
# First, you'll need a function that takes a list of args (e.g. from the command line) that launches your component.
def run_client(*args: str) -> None:
    # Ideally, you should lazily import your component code so that it doesn't have to be loaded until necessary.
    from .bg3_client import launch_bg3_client

    # Also, if your component has its own lifecycle, like if it is its own window that can be interacted with,
    # you should use the LauncherComponents.launch helper (which itself calls launch_subprocess).
    # This will create a subprocess for your component, launching it in a separate window from the Archipelago Launcher.
    launch(launch_bg3_client, name="Baldur's Gate 3 Client", args=args)


# You then add this function as a component by appending a Component instance to LauncherComponents.components.
# Now, it will show up in the Launcher with its display name,
# and when the user clicks on the "Open" button, your function will be run.
components.append(
    Component(
        "Baldur's Gate 3 Client",
        func=run_client,
        game_name="Baldur's Gate 3",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)