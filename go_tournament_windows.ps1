Clear-Host

$display_mode = "1"

# Boucle de 0 à 4 (équivalent à {0..4})
foreach ($mapId in 0..4) {
    Write-Host "Arena: $mapId"

    # Boucle sur True et False
    foreach ($initPos in @("True", "False")) {
        # Appel du script Python avec les arguments
        python tetracomposibot.py config_Paintwars "$mapId" "$initPos" "$display_mode"
    }
}