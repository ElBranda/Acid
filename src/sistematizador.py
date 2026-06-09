import pandas as pd
from src import lector as l
from typing import TypedDict, Any
from utils.helper import format_str, dates

# Esquemas
class EmpleadorSchema(TypedDict):
    cuil: str

class CashflowSchema(TypedDict):
    codigo: str
    importe: str
    deb_cred: str

class EmpleadoReciboSchema(TypedDict):
    cuil: str
    nombre: str
    legajo: str
    cbu: str
    forma_pago: str
    fecha_pago: str
    clashflow: list[CashflowSchema]
    cant_dias_trab: str
    aporte_ad_os: str
    contribu_ad_os: str
    remunera_bruta: str
    base_imponible_1: str
    base_imponible_2: str
    base_imponible_3: str
    base_imponible_4: str
    base_imponible_5: str
    base_imponible_6: str
    base_imponible_7: str
    base_imponible_8: str
    base_imponible_9: str
    base_imponible_10: str
    importe_detraer: str

class EmpleadoBDSchema(TypedDict):
    cuil: str
    conyugue: str
    cant_hijos: str
    cct: str
    scvo: str
    cor_redux: str
    tipo_empresa: str
    tipo_operacion: str
    cod_situacion: str
    cod_condicion: str
    cod_actividad: str
    cod_mod_contrata: str
    cod_siniestrado: str
    cod_localida: str
    sit_rev_1: str
    dia_sit_rev_1: str
    sit_rev_2: str
    dia_sit_rev_2: str
    sit_rev_3: str
    dia_sit_rev_3: str
    horas_trab: str
    porcent_aport_ad_ss: str
    contribu_tarea_dif: str
    cod_obra_social: str
    cant_adherentes: str
    base_calc_dif_aporte_os_y_fsr: str
    base_calc_dif_os_y_fsr: str
    remunera_mater_anses: str
    base_calc_dif_aporte_seg_social: str
    base_calc_dif_contribu_seg_social: str
    base_calc_dif_lrt: str

class EmpleadoSchema(TypedDict):
    cuil: str
    nombre: str
    legajo: str
    cbu: str
    forma_pago: str
    fecha_pago: str
    clashflow: list[CashflowSchema]
    conyugue: str
    cant_hijos: str
    cct: str
    scvo: str
    cor_redux: str
    tipo_empresa: str
    tipo_operacion: str
    cod_situacion: str
    cod_condicion: str
    cod_actividad: str
    cod_mod_contrata: str
    cod_siniestrado: str
    cod_localida: str
    sit_rev_1: str
    dia_sit_rev_1: str
    sit_rev_2: str
    dia_sit_rev_2: str
    sit_rev_3: str
    dia_sit_rev_3: str
    cant_dias_trab: str
    horas_trab: str
    porcent_aport_ad_ss: str
    contribu_tarea_dif: str
    cod_obra_social: str
    cant_adherentes: str
    aporte_ad_os: str
    contribu_ad_os: str
    base_calc_dif_aporte_os_y_fsr: str
    base_calc_dif_os_y_fsr: str
    base_calc_dif_lrt: str
    remunera_mater_anses: str
    remunera_bruta: str
    base_imponible_1: str
    base_imponible_2: str
    base_imponible_3: str
    base_imponible_4: str
    base_imponible_5: str
    base_imponible_6: str
    base_imponible_7: str
    base_imponible_8: str
    base_imponible_9: str
    base_calc_dif_aporte_seg_social: str
    base_calc_dif_contribu_seg_social: str
    base_imponible_10: str
    importe_detraer: str

class FechaSchema(TypedDict):
    m: str
    a: str

class EstructuraLSD(TypedDict):
    fecha: FechaSchema
    empleador: EmpleadorSchema
    empleados: list[EmpleadoSchema]
    n_liquidacion: str

# Funciones
def get_systematized_data(path: str) -> EstructuraLSD:
    df = l.get_data_from_excel(path)
    
    res: EstructuraLSD = {
        'fecha': _get_date(list(df.values())[0]),
        'empleador': _get_data_empl(df['Resumen Mensual']),
        'empleados': _get_data_emp(df),
        'n_liquidacion': str(df["Resumen Mensual"].iloc[3,10]).strip()
    }

    return res

def _get_date(df: pd.DataFrame) -> FechaSchema:
    date: FechaSchema = {
        'm': dates[str(df.iloc[5,1]).strip()],
        'a': str(df.iloc[5,2]).strip()
    }

    return date

def _get_data_empl(df: pd.DataFrame) -> EmpleadorSchema:
    empl: EmpleadorSchema = {
        'cuil': str(df.iloc[0, 3]).replace("-","").strip()
    }

    return empl

def _get_data_emp(df: pd.DataFrame) -> list[EmpleadoSchema]:
    emp_BD_list = _get_data_emp_from_BD(df["BD emp"])
    emp_recibo_list = _get_data_emp_from_recibo(df)
    
    mapa_BD = {emp["cuil"]: emp for emp in emp_BD_list}
    emp_list: list[EmpleadoSchema] = []

    for emp_recibo in emp_recibo_list:
        cuil_actual = emp_recibo["cuil"]
        emp_BD = mapa_BD.get(cuil_actual, {})

        emp_completo: EmpleadoSchema = emp_recibo | emp_BD

        emp_list.append(emp_completo)

    return emp_list

def _get_data_emp_from_BD(df: pd.DataFrame) -> list[EmpleadoBDSchema]:
    emp_list: list[EmpleadoBDSchema] = []
    
    for i in range(4, len(df)):
        cuil = str(df.iloc[i,0]).split('.')[0].strip()
        conyugue = "0" if str(df.iloc[i,12]).strip() == "No" else "1"
        cant_hijos = str(df.iloc[i,13]).strip()
        cct = "0" if str(df.iloc[i,77]).strip() == "No" else "1"
        scvo = "0" if str(df.iloc[i,4]).strip() == "No" else "1"
        cor_redux = "0" if str(df.iloc[i,3]).strip() == "No" else "1"
        tipo_empresa = "1"
        tipo_operacion = "0"
        cod_situacion = str(df.iloc[i,5]).strip()
        cod_condicion = str(df.iloc[i,6]).strip()
        cod_actividad = str(df.iloc[i,7]).strip()
        cod_mod_contrata = str(df.iloc[i,8]).strip()
        cod_siniestrado = str(df.iloc[i,9]).strip()
        cod_localidad = str(df.iloc[i,10]).strip()
        sit_rev_1 = str(df.iloc[i,27]).strip() if not pd.isna(df.iloc[i,27]) else "0"
        dia_sit_rev_1 = str(df.iloc[i,28]).strip() if not pd.isna(df.iloc[i,28]) else "0"
        sit_rev_2 = str(df.iloc[i,29]).strip() if not pd.isna(df.iloc[i,29]) else "0"
        dia_sit_rev_2 = str(df.iloc[i,30]).strip() if not pd.isna(df.iloc[i,30]) else "0"
        sit_rev_3 = str(df.iloc[i,31]).strip() if not pd.isna(df.iloc[i,31]) else "0"
        dia_sit_rev_3 = str(df.iloc[i,32]).strip() if not pd.isna(df.iloc[i,32]) else "0"
        horas_trab = "000"
        porcent_aport_ad_ss = "0"
        contribu_tarea_dif = "0"
        cod_obra_social = str(df.iloc[i,2]).strip()
        cant_adherentes = str(df.iloc[i,14]).strip()
        base_calc_dif_aporte_os_y_fsr = "0"
        base_calc_dif_os_y_fsr = "0"
        base_calc_dif_lrt = "0"
        remunera_mater_anses = "0"
        base_calc_dif_aporte_seg_social = "0"
        base_calc_dif_contribu_seg_social = "0"


        emp: EmpleadoBDSchema = {
            "cuil": cuil,
            "conyugue": conyugue,
            'cant_hijos': cant_hijos,
            'cct': cct,
            'scvo': scvo,
            'cor_redux': cor_redux,
            'tipo_empresa': tipo_empresa,
            'tipo_operacion': tipo_operacion,
            'cod_situacion': cod_situacion,
            'cod_condicion': cod_condicion,
            'cod_actividad': cod_actividad,
            'cod_mod_contrata': cod_mod_contrata,
            'cod_siniestrado': cod_siniestrado,
            'cod_localidad': cod_localidad,
            'sit_rev_1': sit_rev_1,
            'dia_sit_rev_1': dia_sit_rev_1,
            'sit_rev_2': sit_rev_2,
            'dia_sit_rev_2': dia_sit_rev_2,
            'sit_rev_3': sit_rev_3,
            'dia_sit_rev_3': dia_sit_rev_3,
            'horas_trab': horas_trab,
            'porcent_aport_ad_ss': porcent_aport_ad_ss,
            'contribu_tarea_dif': contribu_tarea_dif,
            'cod_obra_social': cod_obra_social,
            'cant_adherentes': cant_adherentes,
            'base_calc_dif_aporte_os_y_fsr': base_calc_dif_aporte_os_y_fsr,
            'base_calc_dif_os_y_fsr': base_calc_dif_os_y_fsr,
            'base_calc_dif_lrt': base_calc_dif_lrt,
            'remunera_mater_anses': remunera_mater_anses,
            'base_calc_dif_aporte_seg_social': base_calc_dif_aporte_seg_social,
            'base_calc_dif_contribu_seg_social': base_calc_dif_contribu_seg_social,
        }

        emp_list.append(emp)

    return emp_list

def _get_data_emp_from_recibo(df: pd.DataFrame) -> list[EmpleadoReciboSchema]:
    emp_list: list[EmpleadoReciboSchema] = []

    for sheet_name, sheet_data in df.items():
        if sheet_name.strip() == "Resumen Mensual":
            break

        if ", vac." in sheet_name.strip().lower() or " vac." in sheet_name.strip().lower():
            cuil_vac = str(sheet_data.iloc[7, 6]).replace("-", "").strip()
            cashflow_cols_vac = sheet_data.iloc[:, [20, 21, 22]].dropna(how='all').reset_index(drop=True)
            cashflow_vac = _get_cashflow_emp(cashflow_cols_vac)
            
            empleado_destino = next(
                (emp for emp in emp_list if emp["cuil"] == cuil_vac), 
                None
            )
            
            if empleado_destino is not None:
                empleado_destino["clashflow"].extend(cashflow_vac)
            
            continue

        # Frankenstein: Toma las columnas U, V y W, borra los nan y resetea los index (no sé cómo esto es legal)
        cashflow_cols = sheet_data.iloc[:, [20,21,22]].dropna(how='all').reset_index(drop=True)

        cbu = _get_emp_cbu(sheet_data)
        forma_pago: str

        if cbu == "":
            forma_pago = "1"
        else:
            forma_pago = "3"

        fecha_pago = _get_emp_date(sheet_data)
        legajo = str(sheet_data.iloc[5, 6]).strip()
        cant_dias_trab = _get_emp_worked_days(df["Resumen Mensual"], legajo)
        aporte_ad_os = _get_emp_aporte_ad_os(df["Resumen Mensual"], legajo)
        contribu_ad_os = str(int(aporte_ad_os)*2)
        # remuneacion bruta, bruto con no remu
        # imoprt 1,2,3,5 es sueldo vruto 
        # importe 4,8 completo el sueldo bruto
        # imorte 6,7, cero
        # importe 9, sueldo brutos mas no remu, excepto viatico
        # importe 10, bruto menos impor a deducir
        # las que le siguen al 9, las dos cero
        sueldo_bruto = _get_emp_sueldo_bruto(df["Resumen Mensual"], legajo)
        importe_deducir = _get_emp_importe_deducir(df["Resumen Mensual"], legajo)
        remunera_bruta = _get_emp_remunera_bruta(df["Resumen Mensual"], legajo, ignorar_viatico=True)
        base_imponible_1 = sueldo_bruto
        base_imponible_2 = sueldo_bruto
        base_imponible_3 = sueldo_bruto
        base_imponible_4 = sueldo_bruto
        base_imponible_5 = sueldo_bruto
        base_imponible_6 = "0"
        base_imponible_7 = "0"
        base_imponible_8 = sueldo_bruto
        base_imponible_9 = _get_emp_remunera_bruta(df["Resumen Mensual"], legajo)
        base_imponible_10 = str(int(sueldo_bruto) - int(importe_deducir))
        importe_detraer = importe_deducir
    

        emp: EmpleadoReciboSchema = {
            'cuil': str(sheet_data.iloc[7,6]).replace("-","").strip(),
            'nombre': str(sheet_data.iloc[5, 3]).strip(),
            'legajo': legajo,
            'cbu': cbu,
            'forma_pago': forma_pago,
            'fecha_pago': fecha_pago,
            "clashflow": _get_cashflow_emp(cashflow_cols),
            'cant_dias_trab': cant_dias_trab,
            'aporte_ad_os': aporte_ad_os,
            'contribu_ad_os': contribu_ad_os,
            'remunera_bruta': remunera_bruta,
            'base_imponible_1': base_imponible_1,
            'base_imponible_2': base_imponible_2,
            'base_imponible_3': base_imponible_3,
            'base_imponible_4': base_imponible_4,
            'base_imponible_5': base_imponible_5,
            'base_imponible_6': base_imponible_6,
            'base_imponible_7': base_imponible_7,
            'base_imponible_8': base_imponible_8,
            'base_imponible_9': base_imponible_9,
            'base_imponible_10': base_imponible_10,
            'importe_detraer': importe_detraer
        }

        emp_list.append(emp)

    return emp_list

def _get_emp_date(df: pd.DataFrame) -> str:
    df_str = df.iloc[:, 5].astype(str).apply(format_str)

    date_row_match = df_str[df_str == "fecha:"].index

    if date_row_match.empty:
        raise IndexError(f"No se encontró la Fecha: {date_row_match}")
    
    date_index_target = date_row_match[0]

    date_celda = df.iloc[date_index_target, 6]

    date = date_celda.split(" ")[0].replace("-","")

    return date

def _get_emp_cbu(df: pd.DataFrame) -> str:
    df_str = df.iloc[:, 0].astype(str).apply(format_str)

    cbu_row_match = df_str[df_str == "cbu:"].index

    if cbu_row_match.empty:
        raise IndexError(f"No se encontró el CBU: {cbu_row_match}")
    
    cbu_index_target = cbu_row_match[0]

    cbu_celda = df.iloc[cbu_index_target, 2]

    cbu = str(cbu_celda) if not pd.isna(cbu_celda) else ""

    return cbu

def _get_emp_importe_deducir(df: pd.DataFrame, legajo: str) -> str:
    df_str = df.iloc[5, :].astype(str).apply(format_str)

    importe_deducir_row_match = df_str[df_str == "importe a deducir"].index

    first_col = df.iloc[:, 0].astype(str).str.split(".").str[0].str.strip()
    leg_row_match = first_col[first_col == legajo].index

    if importe_deducir_row_match.empty or leg_row_match.empty:
        raise IndexError(f"No se encontró el importe a deducir o legajo: {importe_deducir_row_match, leg_row_match}")
    
    importe_deducir_index_target = importe_deducir_row_match[0]
    leg_index_target = leg_row_match[0]
    
    id_celda = df.loc[leg_index_target, importe_deducir_index_target]

    importe_deducir = float(id_celda) if not pd.isna(id_celda) else 0.0

    return f"{importe_deducir:.2f}".replace(".", "").replace(",", "")
    

def _get_emp_sueldo_bruto(df: pd.DataFrame, legajo: str) -> str:
    df_str = df.iloc[5, :].astype(str).apply(format_str)

    sueldo_bruto_row_match = df_str[df_str == "sueldo bruto"].index

    first_col = df.iloc[:, 0].astype(str).str.split(".").str[0].str.strip()
    leg_row_match = first_col[first_col == legajo].index

    if sueldo_bruto_row_match.empty or leg_row_match.empty:
        raise IndexError(f"No se encontró el sueldo bruto o legajo: {sueldo_bruto_row_match, leg_row_match}")
    
    sueldo_bruto_index_target = sueldo_bruto_row_match[0]
    leg_index_target = leg_row_match[0]

    sb_celda = df.loc[leg_index_target, sueldo_bruto_index_target]

    sueldo_bruto = float(sb_celda) if not pd.isna(sb_celda) else 0.0

    return f"{sueldo_bruto:.2f}".replace(".", "").replace(",", "")


def _get_emp_remunera_bruta(df: pd.DataFrame, legajo: str, ignorar_viatico: bool = False) -> str:
    '''
    Calcula el sueldo bruto más los no remunerativos.
    Si ignorar_viatico es False y tiene viáticos, los no remunerativos no se suman al bruto.
    '''
    df_str = df.iloc[5, :].astype(str).apply(format_str)
    
    sueldo_bruto_row_match = df_str[df_str == "sueldo bruto"].index
    no_remu_row_match = df_str[df_str == "no remunerativos"].index
    viatico_row_match = df_str[df_str == "viatico"].index
    
    first_col = df.iloc[:, 0].astype(str).str.split(".").str[0].str.strip()
    leg_row_match = first_col[first_col == legajo].index

    if sueldo_bruto_row_match.empty or no_remu_row_match.empty or leg_row_match.empty:
        raise IndexError(f"No se encontró el sueldo bruto, no remuneración o el legajo: {sueldo_bruto_row_match, no_remu_row_match, leg_row_match}")

    sueldo_bruto_index_target = sueldo_bruto_row_match[0]
    no_remu_index_target = no_remu_row_match[0]
    leg_index_target = leg_row_match[0]
    
    sb_celda = df.loc[leg_index_target, sueldo_bruto_index_target]
    nr_celda = df.loc[leg_index_target, no_remu_index_target]
    
    sueldo_bruto = float(sb_celda) if not pd.isna(sb_celda) else 0.0
    no_remu = float(nr_celda) if not pd.isna(nr_celda) else 0.0

    tiene_viatico = False
    if not viatico_row_match.empty and not ignorar_viatico:
        viatico_val = df.loc[leg_index_target, viatico_row_match[0]]
        if not pd.isna(viatico_val) and format_str(viatico_val) != 'no':
            tiene_viatico = True

    if tiene_viatico:
        total = sueldo_bruto
    else:
        total = sueldo_bruto + no_remu

    return f"{total:.2f}".replace(".", "").replace(",", "")

def _get_emp_aporte_ad_os(df: pd.DataFrame, legajo: str) -> str:
    df_str = df.iloc[5, :].astype(str).str.strip().str.lower()
    aporte_ad_os_row_match = df_str[df_str == "aporte adicional o. social"].index
    first_col = df.iloc[:, 0].astype(str).str.split(".").str[0].str.strip()
    leg_row_match = first_col[first_col == legajo].index

    if leg_row_match.empty:
        raise IndexError(f"No se encontró el legajo para el aporte adicional o. social: {leg_row_match}")

    if aporte_ad_os_row_match.empty:
        raise IndexError(f"No se encontró la columna aporte adicional o. social: {aporte_ad_os_row_match}")

    aporte_ad_os_index_target = aporte_ad_os_row_match[0]
    leg_index_taget = leg_row_match[0]
    aporte_ad_os = f"{float(df.loc[leg_index_taget, aporte_ad_os_index_target]):.2f}".replace(".", "").replace(",","")
    return aporte_ad_os

def _get_emp_worked_days(df: pd.DataFrame, legajo: str) -> str:
    first_col = df.iloc[:, 0].astype(str).str.split(".").str[0].str.strip()
    row_match = first_col[first_col == legajo].index

    if not row_match.empty:
        index_target = row_match[0]
        days_worked = str(df.iloc[index_target,2])

        return days_worked
    else:
        raise IndexError(f"No se encontró el legajo solicitado: {row_match}")


def _get_cashflow_emp(df: pd.DataFrame) -> list[CashflowSchema]:
    cashflow_list: list[CashflowSchema] = []

    for _, data in df.iterrows():
        cashflow: CashflowSchema = {
            'codigo': str(data.iloc[0]),
            'importe': f"{float(data.iloc[1]):.2f}".replace(",","").replace(".",""),
            'deb_cred': str(data.iloc[2])
        }

        cashflow_list.append(cashflow)
    
    return cashflow_list

