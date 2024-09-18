def maps_class(class_int):

    D_map = {
            0 : "TRM",
            1 : "INF",
            2 : "NEOP",
            3 : "EN/IM",
            4 : "EMO",
            5 : "MENT",
            6 : "NERV",
            7 : "CARD",
            8 : "RESP",
            9 : "DIG",
            10 : "GEN",
            11 : "GRAV",
            12 : "CT/CNN",
            13 : "LOC",
            14 : "MALF",
            15 : "P.NAT",
            16 : "MAL"
            }

    return D_map[class_int]

def maps_class_long(class_int):

    D_map = {
            0 : "Traumatismi e avvelenamenti (800-999)",
            1 : "Malattie infettive e parassitarie (001-139) ",
            2 : "Tumori (140-239)",
            3 : "Malattie delle ghiandole endocrine, della nutrizione e del metabolismo, e disturbi immunitari (240-279)",
            4 : "Malattie del sangue e organi emopoietici (280-289)",
            5 : "Disturbi mentali (290-319)",
            6 : "Malattie del sistema nervoso e degli organi di senso (320-389) ",
            7 : "Malattie del sistema circolatorio (390-459)",
            8 : "Malattie dell’apparato respiratorio (460-519)",
            9 : "Malattie dell’apparato digerente (520-579)",
            10 : "Malattie dell’apparato genitourinario (580-629)",
            11 : "Complicazioni della gravidanza, del parto e del puerperio (630-677)",
            12 : "Malattie della pelle e del tessuto sottocutaneo (680-709)",
            13 : "Malattie del sistema osteomuscolare e del tessuto connettivo (710-739) ",
            14 : "Malformazioni congenite (740-759)",
            15 : "Alcune condizioni morbose di origine perinatale(760-779)",
            16 : "Sintomi, segni, e stati morbosi maldefiniti (780-799)"
            }

    return D_map[class_int]

def map_symptoms(symp_int):
        return True