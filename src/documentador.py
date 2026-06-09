from src import sistematizador as s
from src.sistematizador import EstructuraLSD, EmpleadoSchema, CashflowSchema

def printer(path: str) -> None:
    print(s.get_systematized_data(path))

def generate_LSD(filepath: str, outpath: str):
    systemetized_data = s.get_systematized_data(filepath)

    with open(outpath, "w", encoding='latin-1') as file:
        first_line = _generate_first_line(systemetized_data)

        file.write(first_line)

        for emp in systemetized_data["empleados"]:
            second_line = _generate_second_line(emp)
            file.write(second_line)

        for emp in systemetized_data["empleados"]:
            for cashflow in emp["clashflow"]:
                third_line = _generate_third_line(emp, cashflow)
                file.write(third_line)
        
        for emp in systemetized_data["empleados"]:
            fourth_line = _generate_fourth_line(emp)
            file.write(fourth_line)
    
def _generate_first_line(sd: EstructuraLSD) -> str:
    return "01" + sd["empleador"]["cuil"] + "SJ" + sd["fecha"]["a"] + sd["fecha"]["m"] + "M" + sd["n_liquidacion"].zfill(5) + "30" + str(len(sd["empleados"])).zfill(6)

def _generate_second_line(emp: EmpleadoSchema) -> str:
    return "\n" + "02" + emp["cuil"] + emp["legajo"].ljust(60) + emp["cbu"].ljust(22) + "000" + emp["fecha_pago"] + emp["forma_pago"].rjust(9)

def _generate_third_line(emp: EmpleadoSchema, cf: CashflowSchema) -> str:
    return "\n" + "03" + emp["cuil"] + cf["codigo"].ljust(10) + "00000 " + cf["importe"].zfill(15) + cf["deb_cred"] + "".ljust(6)

def _generate_fourth_line(emp: EmpleadoSchema) -> str:
    return "\n" + "04" + emp["cuil"] + emp["conyugue"] + emp["cant_hijos"].zfill(2) + emp["cct"] + emp["scvo"] + emp["cor_redux"] + emp["tipo_empresa"] + emp["tipo_operacion"] + emp["cod_situacion"].zfill(2) + emp["cod_condicion"] + " " + emp["cod_actividad"].zfill(3) + emp["cod_mod_contrata"].zfill(3) + emp["cod_siniestrado"] + " " + emp["cod_localidad"].zfill(2) + emp["sit_rev_1"].zfill(2) + emp["dia_sit_rev_1"].zfill(2) + emp["sit_rev_2"].zfill(2) + emp["dia_sit_rev_2"].zfill(2) + emp["sit_rev_3"].zfill(2) + emp["dia_sit_rev_3"].zfill(2) + emp["cant_dias_trab"].zfill(2) + emp["horas_trab"].zfill(3) + emp["porcent_aport_ad_ss"].zfill(5) + emp["contribu_tarea_dif"].zfill(5) + emp["cod_obra_social"].zfill(6) + emp["cant_adherentes"].zfill(2) + emp["aporte_ad_os"].zfill(15) + emp["contribu_ad_os"].zfill(15) + emp["base_calc_dif_aporte_os_y_fsr"].zfill(15) + emp["base_calc_dif_os_y_fsr"].zfill(15) + emp["base_calc_dif_lrt"].zfill(15) + emp["remunera_mater_anses"].zfill(15) + emp["remunera_bruta"].zfill(15) + emp["base_imponible_1"].zfill(15) + emp["base_imponible_2"].zfill(15) + emp["base_imponible_3"].zfill(15) + emp["base_imponible_4"].zfill(15) + emp["base_imponible_5"].zfill(15) + emp["base_imponible_6"].zfill(15) + emp["base_imponible_7"].zfill(15) + emp["base_imponible_8"].zfill(15) + emp["base_imponible_9"].zfill(15) + emp["base_calc_dif_aporte_seg_social"].zfill(15) + emp["base_calc_dif_contribu_seg_social"].zfill(15) + emp["base_imponible_10"].zfill(15) + emp["importe_detraer"].zfill(15)