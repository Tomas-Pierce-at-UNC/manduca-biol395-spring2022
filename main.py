
import meniscus
import proboscis


def measure_file(out: str, filename: str, start: int = 0, end: int = None):
    mens_masks = meniscus.isolate(filename, start, end)
    probs_masks = proboscis.isolate(filename, start, end)
    for i in range(start, end):
        meniscus_mask = next(mens_masks)
        tongue_mask = next(probs_masks)
        meniscus_canidates = meniscus.get_canidates(meniscus_mask)
        tongue_canidates = proboscis.get_canidates(tongue_mask)
        meniscus_pos = meniscus.select(meniscus_canidates)
        tongue_pos = proboscis.select(tongue_canidates)
        meniscus_measurement = meniscus.measure(meniscus_pos)
        proboscis_measurement = proboscis.measure(tongue_pos)
        with open(out, "a") as handle:
            line = "p {} m {}\n".format(proboscis_measurement,
                                        meniscus_measurement
                                        )
            handle.write(line)


def measure_targets(targetfile: str):
    pass
