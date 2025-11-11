# Multiple Response Keys Configuration

## Overview

The MID Task now accepts multiple keys for responses, allowing users to choose which key they prefer: **space, j, g, f, h**

## Configuration

The response keys are configured in `mid_config.yml`:

```yaml
task:
  resp_keys: ["space", "j", "g", "f", "h"]
```

## How It Works

### Valid Response Keys

During the target presentation phase, participants can press any of these keys:
- **Space bar** (spacebar)
- **j** key
- **g** key
- **f** key
- **h** key

The first valid key press within the response window is recorded with:
- Response time (RT in milliseconds)
- Which key was pressed

### All Versions Support Multiple Keys

✅ **PsychoPy Version** (`mid_psychopy_pc_yaml.py`)  
✅ **Web Version** (`mid_web.js`)  
✅ **Electron Version** (`mid_web_electron.js`)  

## Customization

To change which keys are accepted, edit `mid_config.yml`:

```yaml
task:
  resp_keys: ["space", "j", "g", "f", "h"]  # Add or remove keys here
```

### Examples

**Only spacebar:**
```yaml
resp_keys: ["space"]
```

**Arrow keys:**
```yaml
resp_keys: ["left", "right", "up", "down"]
```

**Number keys:**
```yaml
resp_keys: ["1", "2", "3"]
```

**Mix of keys:**
```yaml
resp_keys: ["space", "return", "a", "b"]
```

## Why Multiple Keys?

✅ **Flexibility** - Users can choose their preferred key  
✅ **Ergonomics** - Different hand positions work for different setups  
✅ **Accessibility** - Accommodates different keyboard layouts  
✅ **Comfort** - Reduces fatigue in long experiments  

## Implementation Details

### Web/Electron Versions

The code checks each pressed key against the valid keys list:

```javascript
const validKeys = config.task.resp_keys || ['space'];

for (const key of currentKeys) {
    if (validKeys.includes(key) || key === ' ' && validKeys.includes('space')) {
        responded = true;
        rt = Math.round(elapsed);
        keyname = key === ' ' ? 'space' : key;
        break;
    }
}
```

**Note:** The spacebar can be pressed as either `' '` or `'space'` and both are recognized.

### PsychoPy Version

```python
elif key == 'space' or key in cfg['task']['resp_keys']:
    keyname = key
    rt_sec = clock.getTime()
    rt = int(rt_sec * 1000.0)
    break
```

## Data Recording

The pressed key is recorded in the data file in the `key` column:
- `space` - if spacebar was pressed
- `j` - if j key was pressed
- `g` - if g key was pressed
- `f` - if f key was pressed
- `h` - if h key was pressed

This allows analysis of:
- Whether users have a key preference
- Response time differences between keys
- User strategy

## Backward Compatibility

Old configurations with only `["space"]` continue to work perfectly. The default fallback is always `["space"]` if no keys are configured.

## Testing

To test multiple keys:

1. Run the experiment
2. During target presentation, try pressing different keys (j, g, f, h, space)
3. Verify that any of these keys registers as a valid response
4. Check the data file to see which key was recorded

## Escape Key

The **Escape** key is always reserved for exiting the experiment and is not used for responses.

