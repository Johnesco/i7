"Babel Fish Puzzle Permutation 2013 - An Homage To Adams and Meretzky" by Taupelink

Vogon Hold is a room.
The description of Vogon Hold is "A squalid room. Along one wall is a dispenser. A large fan, built in to the floor, intermittently blasts a jet of air up into the room. You have items in your inventory. An intercom repeats an unintelligible three-word phrase."

The dispenser is fixed in place scenery in Vogon Hold.
The description of the dispenser is "It has a button."

The button is part of the dispenser.

The player is carrying a gown, a towel, a satchel, and a loose pile of mail.

The satchel is a supporter.

A metal hook, a drain, a large fan, and a panel are fixed in place scenery supporters in Vogon Hold.

Fitting relates one thing (called the correspondent) to one supporter.
The verb to fit (he fits, they fit, he fitted, it is fitted, he is fitting) implies the fitting relation.

Gown fits hook.
Towel fits drain.
Satchel fits panel.
Mail fits fan.

Check putting it on:
	if the noun is not the correspondent of the second noun, say "That doesn't seem to fit." instead.

To say shoots:
	say "A Babel fish shoots out of the dispenser. It arcs downward."

To say GownSucceeds:
	say "[SatchelSucceeds]The Babel fish bounces off of the gown. It is lifted[if mail is on fan] into a cloud of junk mail[otherwise] toward the ceiling[end if] by a sudden gust from the fan. An airborne robot flies into the room."

To say TowelSucceeds:
	say "[shoots]The Babel fish lands on the towel. A floorborne robot appears, grabs the fish, and whizzes toward a panel in the wall."

To say SatchelSucceeds:
	say "[TowelSucceeds]The floor robot plows into the satchel, sending the Babel fish flying[if mail is on satchel] surrounded by a cloud of mail[end if]. It continues flying."

To say MailSucceeds:
	say "[GownSucceeds]The air robot starts collecting the plume of mail. The fish is ignored."

Instead of pushing the button when the towel is not on the drain:
	say "[shoots]It falls into a drain."

Instead of pushing the button when the towel is on the drain and the satchel is not on the panel:
	say "[TowelSucceeds]The floor robot zips through the panel."

Instead of pushing the button when the towel is on the drain and the satchel is on the panel and the gown is not on the hook:
	say "[SatchelSucceeds]It sails through a small hole in the wall, just under a metal hook."

Instead of pushing the button when the towel is on the drain and the satchel is on the panel and the gown is on the hook and the mail is not on the fan:
	say "[GownSucceeds]The air robot catches the Babel fish (which is all the flying junk it can find) and exits."

Instead of pushing the button:
	say "[MailSucceeds]The Babel fish lands in your ear. You can suddenly understand the announcement on the intercom. It says:";
	end the story saying "[bold type]You have won[roman type]".

Understand "hang [a thing] on [a supporter]" as putting it on.
Understand "cover [a supporter] with [a thing]" as putting it on (with nouns reversed).
Understand "put [a thing] in front of [a supporter]" as putting it on.

Test me with "examine dispenser / push button / inventory / cover drain with towel / push button / put satchel in front of panel / push button / hang gown on hook / push button / put mail on fan / push button".
