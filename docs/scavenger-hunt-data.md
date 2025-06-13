# Scavenger Hunt Data

## Milwaukee Scavenger Hunt Steps

This file contains the 13 steps for the Milwaukee scavenger hunt as specified in the requirements.

```javascript
const scavengerHuntSteps = [
  {
    id: 1,
    name: "Black Cat Alley",
    clue: "Find the place where cats don't purr — they pop with color on the wall for sure.",
    qrCodeUrl: "URL_TO_QR_CODE_1", // To be replaced with actual QR code URL
    qrCodeValue: "BLACKCAT_ALLEY_001" // Unique identifier for validation
  },
  {
    id: 2,
    name: "Milwaukee Art Museum",
    clue: "What flaps like a bird but never flies? Find the building that spreads its wings by the lake.",
    qrCodeUrl: "URL_TO_QR_CODE_2",
    qrCodeValue: "ART_MUSEUM_002"
  },
  {
    id: 3,
    name: "Discovery World",
    clue: "Where science meets the sea, you'll find a big ship and tech to see.",
    qrCodeUrl: "URL_TO_QR_CODE_3",
    qrCodeValue: "DISCOVERY_WORLD_003"
  },
  {
    id: 4,
    name: "Lakeshore State Park",
    clue: "A park on water — now that's rare! Find the trail with skyline flair.",
    qrCodeUrl: "URL_TO_QR_CODE_4",
    qrCodeValue: "LAKESHORE_PARK_004"
  },
  {
    id: 5,
    name: "Pierhead Lighthouse",
    clue: "It's red and bright and guards the shore, you'll find it near the lakeside floor.",
    qrCodeUrl: "URL_TO_QR_CODE_5",
    qrCodeValue: "PIERHEAD_LIGHT_005"
  },
  {
    id: 6,
    name: "Historic Third Ward",
    clue: "Old warehouses with modern flair, boutiques and murals everywhere!",
    qrCodeUrl: "URL_TO_QR_CODE_6",
    qrCodeValue: "THIRD_WARD_006"
  },
  {
    id: 7,
    name: "The Hop - Historic Third Ward Stop",
    clue: "You don't need a ticket, just wait for the ride. Find the streetcar track and pose with pride!",
    qrCodeUrl: "URL_TO_QR_CODE_7",
    qrCodeValue: "HOP_STATION_007"
  },
  {
    id: 8,
    name: "Milwaukee Public Market",
    clue: "Inside this market, smells float in the air — find cheese, spice, or chocolate fair!",
    qrCodeUrl: "URL_TO_QR_CODE_8",
    qrCodeValue: "PUBLIC_MARKET_008"
  },
  {
    id: 9,
    name: "Gertie the Duck Statue",
    clue: "She once sat beneath a bridge, a wartime hero with a nest to rig.",
    qrCodeUrl: "URL_TO_QR_CODE_9",
    qrCodeValue: "GERTIE_DUCK_009"
  },
  {
    id: 10,
    name: "The Bronze Fonz",
    clue: '"Ayyyy!" is what he\'d say — find this cool guy by the river today.',
    qrCodeUrl: "URL_TO_QR_CODE_10",
    qrCodeValue: "BRONZE_FONZ_010"
  },
  {
    id: 11,
    name: "Marcus Performing Arts Center",
    clue: "Music and drama live here night and day. Find a poster or sculpture on display!",
    qrCodeUrl: "URL_TO_QR_CODE_11",
    qrCodeValue: "MARCUS_ARTS_011"
  },
  {
    id: 12,
    name: "Milwaukee City Hall",
    clue: "With its tall clock tower and historic face, this building stands with elegant grace.",
    qrCodeUrl: "URL_TO_QR_CODE_12",
    qrCodeValue: "CITY_HALL_012"
  },
  {
    id: 13,
    name: "The Pfister Hotel / Blu Lounge",
    clue: "Time to celebrate your final clue — find the place with a stunning view.",
    qrCodeUrl: "URL_TO_QR_CODE_13",
    qrCodeValue: "PFISTER_HOTEL_013"
  }
];
```

## QR Code Generation Notes

For testing and deployment, QR codes should be generated with the following values:
- Each QR code should contain the `qrCodeValue` as its data
- QR codes should be placed at the actual locations in Milwaukee
- For testing purposes, we can generate QR codes with these values
- Admin interface will allow updating QR code URLs as needed

## Location Details

### Black Cat Alley
- Address: 1134 E Brady St, Milwaukee, WI 53202
- Description: Street art alley with colorful murals

### Milwaukee Art Museum
- Address: 700 N Art Museum Dr, Milwaukee, WI 53202
- Description: Famous for its wing-like Burke Brise Soleil

### Discovery World
- Address: 500 N Harbor Dr, Milwaukee, WI 53202
- Description: Science and technology museum with the S/S Denis Sullivan

### Lakeshore State Park
- Address: 500 N Harbor Dr, Milwaukee, WI 53202
- Description: Urban island park with city skyline views

### Pierhead Lighthouse
- Address: 500 N Harbor Dr, Milwaukee, WI 53202
- Description: Historic red lighthouse at the harbor

### Historic Third Ward
- Address: Third Ward, Milwaukee, WI
- Description: Historic warehouse district with shops and galleries

### The Hop - Historic Third Ward Stop
- Address: 333 N Water St, Milwaukee, WI 53202
- Description: Streetcar system stop

### Milwaukee Public Market
- Address: 400 N Water St, Milwaukee, WI 53202
- Description: Indoor market with local vendors

### Gertie the Duck Statue
- Address: Riverwalk near Wisconsin Ave Bridge
- Description: Bronze statue commemorating a famous duck

### The Bronze Fonz
- Address: 117 E Wells St, Milwaukee, WI 53202
- Description: Bronze statue of the Fonzie character

### Marcus Performing Arts Center
- Address: 929 N Water St, Milwaukee, WI 53202
- Description: Premier performing arts venue

### Milwaukee City Hall
- Address: 200 E Wells St, Milwaukee, WI 53202
- Description: Historic building with distinctive clock tower

### The Pfister Hotel / Blu Lounge
- Address: 424 E Wisconsin Ave, Milwaukee, WI 53202
- Description: Historic luxury hotel with rooftop views

