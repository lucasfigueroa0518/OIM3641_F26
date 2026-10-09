"""Pull people and companies out of inbound lead notes."""

import time

from transformers import pipeline

NOTES = [
    "Hi, I'm Maya Chen from Northwind Logistics. We need a CRM that can score inbound leads from our website.",
    "Please stop emailing me. This is Jordan Patel at Helios and we already have a vendor.",
    "Sarah Okonkwo at Brightline Capital asked for pricing on a 50-seat plan.",
]

LABELS = {
    "PER": "person",
    "ORG": "company",
    "LOC": "place",
    "MISC": "other",
}


def main() -> None:
    started = time.perf_counter()
    ner = pipeline(
        "token-classification",
        model="dslim/bert-base-NER",
        aggregation_strategy="simple",
    )
    load_seconds = time.perf_counter() - started
    print(f"model_load_seconds={load_seconds:.1f}")
    print()

    for note in NOTES:
        print(note)
        found = ner(note)
        if not found:
            print("  (no entities)")
        for entity in found:
            kind = LABELS.get(entity["entity_group"], entity["entity_group"])
            print(f"  {kind:8} {entity['word']:28} {entity['score']:.0%}")
        print()


if __name__ == "__main__":
    main()
