# Components and Controls

## When to use

Use for buttons, inputs, forms, navigation, dialogs, menus, tooltips, tables, reusable primitives, state APIs, and interaction polish.

## Inputs

- user action, frequency, risk, permissions, and async behavior;
- existing component library, primitives, variants, tokens, and conventions;
- semantic HTML requirements and keyboard interaction pattern;
- validation rules, server errors, destructive consequences, and loading behavior.

## Component procedure

1. **Start from semantics.** Choose the native element and interaction pattern before styling.
2. **Reuse trusted primitives.** Prefer the repository's accessible dialog, menu, select, combobox, popover, tabs, and tooltip implementations.
3. **Model states.** Define state transitions, ownership, async outcomes, and invalid combinations.
4. **Design the anatomy.** Name stable slots such as trigger, label, description, content, error, and actions.
5. **Choose a small variant API.** Use explicit `variant` and `size` axes. Avoid boolean prop soup and raw style props for every token.
6. **Preserve escape hatches.** Forward refs and appropriate native props; support composition where structure must vary.
7. **Render every state.** Verify focus, long labels, icons, loading, errors, disabled, and destructive confirmation.

## Buttons and actions

- One local action should read as primary. Secondary and tertiary actions recede without becoming ambiguous.
- Use `<button>` for actions and links for navigation. Do not recreate button semantics on a generic element.
- Default reusable buttons to `type="button"`; submit buttons declare `type="submit"` inside a form.
- Label the result: “Save changes,” “Invite member,” “Download report.”
- Give press state immediate feedback without moving the target or causing surrounding layout shift.
- A loading button retains enough width to prevent a jump and exposes busy state programmatically.
- Prevent duplicate submission while preserving feedback and a recovery path.
- Destructive actions are visually distinct, separated from routine confirmation, and name the object and consequence.
- Icon-only buttons require an accessible action name and a tooltip only when the action is not already clear from context.

## Icons

- Use one icon family and a consistent visual weight, cap style, corner language, and optical size.
- Prefer text for unfamiliar or high-stakes actions. An icon does not become understandable through repetition inside one screen.
- Use filled versus outlined state consistently; either can represent selection if the system is coherent.
- Optically center asymmetric marks by correcting the SVG or a documented local offset.
- Simplify icons at small sizes; fine strokes and multi-path detail disappear.
- Keep icon-label gaps consistent and ensure the icon does not dominate the text.
- Icons that convey state need a text equivalent; decorative icons are hidden from assistive technology.

## Forms

- Wrap submit flows in a real `<form>` so Enter works naturally.
- Every input has a persistent, programmatically associated label.
- Use the input type, input mode, autocomplete token, and spellcheck behavior appropriate to the data. Do not disable password managers or autocomplete without a documented product reason.
- Prefixes and suffixes live inside the field geometry. Clickable decorations are buttons; noninteractive decorations do not intercept pointer events.
- Inputs use at least 16px text on mobile contexts where smaller values trigger browser zoom.
- Preserve user input after validation or server failure.
- Place field errors beside the responsible field, set `aria-invalid`, and connect explanatory text with `aria-describedby`.
- Put a form-level summary only when multiple errors or off-screen errors require orientation; it complements inline errors.
- Required, optional, disabled, read-only, and permission-restricted are different states with different semantics.
- Prefill known data when safe, current, and expected. Never expose private information through an inappropriate default.

## Selection controls

- Make the label and the whitespace between label and checkbox/radio part of the hit area.
- Use checkbox for independent selections, radio for one choice in a visible set, switch for an immediate on/off setting, and select/combobox when options need disclosure or search.
- A switch should not require a separate Save unless the product clearly models staged settings.
- Selected, indeterminate, disabled, focus, hover, and error states must remain distinguishable without color alone.
- Avoid auto-advancing multi-field input when it prevents correction, paste, or assistive use.

## Dialogs, menus, and popovers

- Move focus into a modal dialog, contain it, support Escape when safe, and return focus to the trigger.
- Title and describe dialogs programmatically. Initial focus should minimize destructive mistakes.
- Menus implement arrow-key movement and typeahead through a proven primitive.
- Tooltips provide short noninteractive explanations. Interactive content belongs in a popover.
- Delay tooltips enough to prevent incidental activation; once a tooltip sequence is active, reduce repeated delay.
- Keep pointer paths to submenus forgiving. Users should be able to move diagonally without accidental closure.
- Position overlays within the viewport, flip when needed, and test zoom, mobile keyboard, and scroll containers.

## Async feedback

- Use optimistic feedback only when success is likely, the state can be reverted, and conflicts are handled.
- Skeletons reserve known structure; spinners indicate indeterminate work where structure is unavailable.
- Long operations show progress when it can be measured and explain what remains when it cannot.
- Toasts confirm background or cross-location outcomes; inline feedback is better when the action's context remains visible.
- Auto-dismiss duration must allow reading and must pause on hover, focus, or hidden tabs where loss matters.
- Copy actions confirm success briefly without removing the accessible name.

## Component API rules

- Prefer composition for variable structure and variants for bounded visual choices.
- Use positive, consistent prop names and conventional `onX` event handlers.
- Avoid configuration objects that duplicate ordinary JSX structure.
- Support controlled and uncontrolled modes only when both are real use cases; document state ownership.
- Do not abstract after one occurrence. Extract when repetition reveals a stable contract or shared behavior.
- Keep public APIs shallow and difficult to misuse. Invalid state combinations should be impossible or rejected.

## Completion

Native semantics and keyboard patterns are correct, all real states render without layout shift, labels and errors are connected, destructive and async behavior is explicit, hit areas are usable, and the component API expresses valid choices without accidental complexity.

## Escalate

Escalate destructive behavior without a defined recovery policy, ambiguous server validation, permission models that cannot be represented truthfully, or requests to replace a trusted accessible primitive without equivalent testing.
