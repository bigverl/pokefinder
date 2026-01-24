
    # def _build_versus_types_table(self, pokemon_names: frozenset[str]) -> VersusTypesTable:
    #     """Build versus types table showing offensive type matchups for each pokemon."""
    #     versus_rows = []
    #     for name in sorted(pokemon_names):
    #         # Find which types this Pokemon has
    #         pokemon_types = []
    #         type_index = self.repository.get_type_index()
    #         for type_name, pokemon_set in type_index.items():
    #             if name in pokemon_set:
    #                 pokemon_types.append(type_name)

    #         type_str = "/".join(pokemon_types)
    #         effectiveness = self.repository.get_type_effectiveness(*pokemon_types)

    #         versus_rows.append(VersusTypesTableRow(
    #             name=name,
    #             type_combo=type_str,
    #             four_x=", ".join(sorted(effectiveness.get("4x", []))) or "-",
    #             two_x=", ".join(sorted(effectiveness.get("2x", []))) or "-",
    #             one_x=", ".join(sorted(effectiveness.get("1x", []))) or "-",
    #             half_x=", ".join(sorted(effectiveness.get("0.5x", []))) or "-",
    #             zero_x=", ".join(sorted(effectiveness.get("0x", []))) or "-"
    #         ))
    #         # THIS NEEDS TO BE CHANGED TO BE REVERSED AND PROBABLY RENAMED TO "OFFENSIVE"
    #         # ALSO, I THINK WE NEED TO REEXAMINE THE TYPE MATCHUPS FIXTURE SCRIPT BECAUSE IT
    #         # DOESNT INCLUDE 0.25. RIP
    #     return VersusTypesTable(rows=versus_rows)