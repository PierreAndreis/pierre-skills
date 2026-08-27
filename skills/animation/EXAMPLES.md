# Animation Examples

## Cut brief

```markdown
## Motion brief — command palette highlight

**Verdict:** cut
**Trigger and frequency:** arrow keys, dozens to hundreds of times per day
**Purpose:** state indication already exists through immediate highlight position
**Interruption:** every keypress must track one-to-one
**Reduced motion:** identical instant update
**Mechanism:** no transition
**Open risk:** none; latency is more harmful than ornament here
```

## Build brief

```markdown
## Motion brief — account popover

**Verdict:** animate
**Trigger and frequency:** pointer or keyboard activation, occasional
**Purpose:** connect the floating surface to its trigger and soften appearance
**Enter / exit:** opacity plus a near-full scale; exit mirrors enter and is shorter
**Origin / direction:** primitive-provided transform origin at the trigger
**Easing + duration:** strong deceleration, tuned around 170ms
**Interruption:** CSS transition reverses from the current state
**Reduced motion:** opacity only
**Mechanism:** primitive state attributes plus CSS transition
**Open risk:** verify rapid reopen and narrow touch viewport
```

## Review finding

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | Name only the changed composite properties | Prevent unrelated layout or paint work |
| A drawer keyframe restarts on reversal | Use an interruptible transition or spring | The surface should continue from its current position |
| Reduced mode retains horizontal travel | Keep only the state-changing fade | Reduced motion must remove movement, not merely shorten it |

**Verdict: Block** until rapid reversal and the reduced-motion variant are observed in the running interface.
