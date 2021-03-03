# -*- coding: utf-8 -*-
"""
fordev.generators
-----------------

This module collects the random data generated by the 4devs website
and provides a simple interface for use.

Use help function for more information:

>>> from fordev import generators
>>> help(generators)
Help on module fordev.generators in fordev:

NAME
    fordev.generators

DESCRIPTION
(...)

Or consult the official documentation.

Note
----
Most of the functions of the ``fordev.generators`` module contain parameters
in common, they are ``uf_code``, ``formatting`` and ``data_only``.

More details in next section.

Parameters
----------
uf_code: str
    UF(Unidade Federativa) code for generating data.
    
    More info about UF: https://pt.wikipedia.org/wiki/Subdivis%C3%B5es_do_Brasil

formatting: bool
    If ``True``, returns formatted data. 
    If it is ``False``, there is no formatted data.

data_only: bool
    If ``True``, return data only. If ``False``, return msg and data or error.

OBS: These are common parameters in the functions
of the ``fordev.generators`` module.
"""

__all__ = [
    'certificate',
    'cnh',
    'bank_account',
    'cpf',
    'pis_pasep',
    'renavam',
    'vehicle',
    'vehicle_brand',
    'vehicle_plate',
    'cnpj',
    'rg',
    'state_registration',
    'voter_title',
    'credit_card',
    'people',
    'company',
    'uf',
    'city'
]

from .__about__ import __version__
from .__about__ import __author__
from .__about__ import __email__
from .__about__ import __github__

from json import loads as json_loads

from random import sample as random_sample
from random import choice as random_choice

from .core import fordev_request

from .consts import ALL_UF_CODE
from .consts import ALL_VEHICLE_BRANDS
from .consts import ALL_BANK_FLAGS

from .validators import raise_for_invalid_uf

from .filters import data_format
from .filters import filter_city_name
from .filters import filter_vehicle_info
from .filters import filter_credit_card_info
from .filters import filter_bank_account_info
from .filters import filter_company_info


def certificate(type_: str='I', formatting: bool=True, data_only: bool=True) -> str:
    """Random generate of certificate(birth, wedding, religious wedding and death).
    
    Parameter
    ---------
    type_
        Type of certificate generate.
            Options: 
                'B' = Birth
                'W' = Wedding
                'R' = Religious Wedding
                'D' = Death
                'I' = Indifferent (Default)
    """

    type_ = type_.upper()

    certificate_types = {'I': 'Indiferente', 'B': 'nascimento', 'W': 'casamento', 'R': 'casamento_religioso', 'D': 'obito'}

    # If type_ not exists in certificate_types, raise exception.
    if not certificate_types.get(type_, False):
        msg_error = f'The certificate type "{type_}" is invalid. Enter a valid type.'
        msg_error += f' Ex: "B" = Birth, "W" = Wedding, "R" = Religious Wedding, "D" = Death and "I" = Indifferent (Default).'

        raise ValueError(msg_error)

    r = fordev_request(
        content_length=67,  # Max of bytes for generate certificate in all possibilities.
        referer='gerador_numero_certidoes', 
        payload={
            'acao': 'gerador_certidao',
            'pontuacao': 'S' if formatting else 'N',
            'tipo_certidao': certificate_types.get(type_)
        }
    )

    return data_format(data_only=data_only, data_dict=r)


def cnh(data_only: bool=True) -> str:
    """Random generate of CNH(Carteira Nacional de Habilitação)."""

    r = fordev_request(
        content_length=14,
        referer='gerador_de_cnh',
        payload={'acao': 'gerar_cnh'}
    )

    return data_format(data_only=data_only, data_dict=r)


def bank_account(bank: int=0, uf_code: str='', data_only: bool=True) -> dict:
    """Generate random bank account information.
    
    Parameter
    ---------
    bank
        Flag of the bank that wants to generate the account information.
            Options:
                0 = Random
                1 = Banco do Brasil
                2 = Bradesco
                3 = Citibank
                4 = Itaú
                5 = Santander
    """

    if not (0 <= bank <= 5):
        msg_error = f'The bank code value "{bank}" is invalid. Enter a valid bank code.'
        msg_error += f' The range is 0 to 5.'

        raise ValueError(msg_error)

    # Replace the bank number with the bank code used in 4devs.
    bank = ['', 2, 121, 85, 120, 151][bank]  # Use the index for get the bank code.

    uf_code = uf_code.upper()

    raise_for_invalid_uf(uf=uf_code, include_blank=True)

    r = fordev_request(
        content_length=45,
        referer='gerador_conta_bancaria',
        payload={
            'acao': 'gerar_conta_bancaria',
            'estado': uf_code,
            'banco': bank
        }
    )
    
    # Replace data in html format with bank account info only.
    r['data'] = filter_bank_account_info(r['data'])
    
    return data_format(data_only=data_only, data_dict=r)


def cpf(uf_code: str='', formatting: bool=True, data_only: bool=True) -> str:
    """Random generate of CPF(Cadastro de Pessoas Físicas)."""

    uf_code = uf_code.upper()

    raise_for_invalid_uf(uf=uf_code, include_blank=True)

    r = fordev_request(
        content_length=38 if uf_code == '' else 40,
        referer='gerador_de_cpf',
        payload={
            'acao': 'gerar_cpf',
            'pontuacao': 'S' if formatting else 'N',
            'cpf_estado': uf_code
        }
    )

    return data_format(data_only=data_only, data_dict=r)


def pis_pasep(formatting: bool=True, data_only: bool=True) -> str:
    """Random generate of PIS/PASEP code."""

    r = fordev_request(
        content_length=26,
        referer='gerador_de_pis_pasep',
        payload={
            'acao': 'gerar_pis',
            'pontuacao': 'S' if formatting else 'N'
        }
    )
    
    return data_format(data_only=data_only, data_dict=r)    


def renavam(data_only: bool=True) -> str:
    """Random generate of RENAVAM(Registro Nacional de Veículos Automotores) code."""

    r = fordev_request(
        content_length=18,
        referer='gerador_de_renavam',
        payload={'acao': 'gerar_renavam'}
    )

    return data_format(data_only=data_only, data_dict=r) 


def vehicle(brand_code: int=0, uf_code: str='', formatting: bool=True, data_only: bool=True) -> dict:
    """Generate random bank account information.
    
    Parameter
    ---------
    brand
        Flag of the vehicle brand that wants to generate the vehicle information.
            Options:
                0 = Random
                1 = Acura
                2 = Agrale
                3 = Alfa Romeo
                4 = AM Gen
                5 = Asia Motors
                6 = ASTON MARTIN
                7 = Audi
                8 = BMW
                9 = BRM
                10 = Buggy
                11 = Bugre
                12 = Cadillac
                13 = CBT Jipe
                14 = CHANA
                15 = CHANGAN
                16 = CHERY
                17 = Chrysler
                18 = Citroen
                19 = Cross Lander
                20 = Daewoo
                21 = Daihatsu
                22 = Dodge
                23 = EFFA
                24 = Engesa
                25 = Envemo
                26 = Ferrari
                27 = Fiat
                28 = Fibravan
                29 = Ford
                30 = FOTON
                31 = Fyber
                32 = GEELY
                33 = GM - Chevrolet
                34 = GREAT WALL
                35 = Gurgel
                36 = HAFEI
                37 = Honda
                38 = Hyundai
                39 = Isuzu
                40 = JAC
                41 = Jaguar
                42 = Jeep
                43 = JINBEI
                44 = JPX
                45 = Kia Motors
                46 = Lada
                47 = LAMBORGHINI
                48 = Land Rover
                49 = Lexus
                50 = LIFAN
                51 = LOBINI
                52 = Lotus
                53 = Mahindra
                54 = Maserati
                55 = Matra
                56 = Mazda
                57 = Mercedes-Benz
                58 = Mercury
                59 = MG
                60 = MINI
                61 = Mitsubishi
                62 = Miura
                63 = Nissan
                64 = Peugeot
                65 = Plymouth
                66 = Pontiac
                67 = Porsche
                68 = RAM
                69 = RELY
                70 = Renault
                71 = Rolls-Royce
                72 = Rover
                73 = Saab
                74 = Saturn
                75 = Seat
                76 = SHINERAY
                77 = smart
                78 = SSANGYONG
                79 = Subaru
                80 = Suzuki
                81 = TAC
                82 = Toyota
                83 = Troller
                84 = Volvo
                85 = VW - VolksWagen
                86 = Wake
                87 = Walk
    """

    if not (0 <= brand_code <= 87):
        msg_error = f'The vehicle brand code value "{brand_code}" is invalid. Enter a valid vehicle brand code.'
        msg_error += f' The range is 0 to 87.'

        raise ValueError(msg_error)

    # Replace the brand code with the brand code used in 4devs.
    if brand_code != 0:
        brand_code = ALL_VEHICLE_BRANDS[brand_code]['code']
    else:
        brand_code = ''

    uf_code = uf_code.upper()

    raise_for_invalid_uf(uf=uf_code, include_blank=True)

    r = fordev_request(
        content_length=62,  # Max of bytes for generate vehicle data in all possibilities.
        referer='gerador_de_veiculos',
        payload={
            'acao': 'gerar_veiculo',
            'pontuacao': 'S' if formatting else 'N',
            'estado': uf_code,
            'fipe_codigo_marca': brand_code
        }
    )
    
    # Replace data in html format with bank account info only.
    r['data'] = filter_vehicle_info(r['data'])
    
    return data_format(data_only=data_only, data_dict=r)


def vehicle_brand(n: int=1, data_only: bool=True) -> list:
    """Random generation of vehicle brand.

    Parameter
    ---------
    n
        A number of vehicle brand for generate random code. The range is of 1 to 87.
    """

    if not (1 <= n <= 87):
        msg_error = f'The n value "{n}" is invalid. Enter a valid number of UF.'
        msg_error += f' The range is 1 to 27 UF code.'

        raise ValueError(msg_error)
    
    full_data = {
        'msg': 'success', 
        'data': random_sample(
            [v_brand['brand_name'] for v_brand in ALL_VEHICLE_BRANDS.values()],  # Create a list brand name
            n 
        )
    }

    if data_only:
        return full_data['data']
    else:
        return full_data


def vehicle_plate(uf_code: str='', formatting: bool=True, data_only: bool=True) -> str:
    """Generate random Vehicle plate code."""

    uf_code = uf_code.upper()

    raise_for_invalid_uf(uf=uf_code, include_blank=True)

    r = fordev_request(
        content_length=36 if uf_code == '' else 38,
        referer='gerador_de_placa_automoveis',
        payload={
            'acao': 'gerar_placa',
            'pontuacao': 'S' if formatting else 'N',
            'estado':uf_code
        }
    )
    
    return data_format(data_only=data_only, data_dict=r)


def cnpj(formatting: bool=True, data_only: bool=True) -> str:
    """Random generate of CNPJ(Cadastro Nacional da Pessoa Jurídica)."""

    r = fordev_request(
        content_length=27,
        referer='gerador_de_cnpj',
        payload={
            'acao': 'gerar_cnpj',
            'pontuacao': 'S' if formatting else 'N',
        }
    )

    return data_format(data_only=data_only, data_dict=r)


def rg(formatting: bool=True, data_only: bool=True) -> str:
    """Random generate of RG(Registro Geral) of emitter SSP-SP."""

    r = fordev_request(
        content_length=25,
        referer='gerador_de_rg',
        payload={
            'acao': 'gerar_rg',
            'pontuacao': 'S' if formatting else 'N',
        }
    )
    
    return data_format(data_only=data_only, data_dict=r)


def state_registration(uf_code: str='SP', formatting: bool=True, data_only: bool=True) -> str:
    """Generate random state registration code."""

    uf_code = uf_code.upper()

    raise_for_invalid_uf(uf=uf_code)

    r = fordev_request(
        content_length=35,
        referer='gerador_de_inscricao_estadual',
        payload={
            'acao': 'gerar_ie',
            'pontuacao': 'S' if formatting else 'N',
            'estado': uf_code
        }
    )
    
    return data_format(data_only=data_only, data_dict=r)


def voter_title(uf_code: str, data_only: bool=True) -> str:
    """Random generation of Voter Title for the selected state."""

    uf_code = uf_code.upper()

    raise_for_invalid_uf(uf=uf_code)

    r = fordev_request(
        content_length=35,
        referer='gerador_de_titulo_de_eleitor',
        payload={
            'acao': 'gerar_titulo_eleitor',
            'estado': uf_code
        }
    )

    return data_format(data_only=data_only, data_dict=r)


def credit_card(bank: int=0, formatting: bool=True, data_only: bool=True) -> dict:
    """Generate random credit card information.
    
    Parameter
    ---------
    bank
        Flag of the bank that wants to generate the credit card information.
            Options:
                0 = Random
                1 = MasterCard
                2 = Visa 16 Dígitos
                3 = American Express
                4 = Diners Club
                5 = Discover
                6 = enRoute
                7 = JCB
                8 = Voyager
                9 = HiperCard
                10 = Aura
    """

    if not (0 <= bank <= 10):
        msg_error = f'The bank code value "{bank}" is invalid. Enter a valid bank code.'
        msg_error += f' The range is 0 to 10.'

        raise ValueError(msg_error)

    # Replace the bank code with the bank flag used in 4devs.
    if bank != 0:
        bank = ALL_BANK_FLAGS[bank]
    else:
        bank = random_choice(
            list(ALL_BANK_FLAGS.values())
        ) 

    r = fordev_request(
        content_length=43,
        referer='gerador_de_numero_cartao_credito',
        payload={
            'acao': 'gerar_cc',
            'pontuacao': 'S' if formatting else 'N',
            'bandeira': bank
        }
    )
    
    # Replace data in html format with credit card info only.
    r['data'] = filter_credit_card_info(r['data'])

    return data_format(data_only=data_only, data_dict=r)


def people(
        n: int=1,
        sex: str='R',
        age: int=0,
        uf_code: str='',
        formatting: bool=True,
        data_only: bool=True
    ) -> str:
    """Random generation of people data.
    
    Parameters
    ----------
    n
        The number of people data generated. The range is 1 to 30 peoples.

    sex
        "M", "F" or "R" is equal a "Male", "Feminine" and "Random" respectively. <Default is "R">

    age
        Age of people generated. The range is 18 to 80 age.
    """
    
    sex = sex.upper()

    uf_code = uf_code.upper()

    if not (1 <= n <= 30):
        msg_error = f'The n value "{n}" is invalid. Enter a valid number of people.'
        msg_error += f' The range is 1 to 30 peoples.'

        raise ValueError(msg_error)

    if sex not in ['M', 'F', 'R']:
        msg_error = f'The sex "{sex}" is invalid. Enter a valid sex.'
        msg_error += f' Ex: "M" = Male, "F" = Feminine or "R" = Random.'

        raise ValueError(msg_error)

    if not (18 <= age <= 80) and age != 0:
        msg_error = f'The age "{age}" is invalid. Enter a valid age.'
        msg_error += f' The range is 18 to 80 age'

        raise ValueError(msg_error)
    
    raise_for_invalid_uf(uf=uf_code, include_blank=True)

    r = fordev_request(
        content_length=99,  # Max of bytes for generate people in all possibilities.
        referer='gerador_de_pessoas',
        payload={
            'acao': 'gerar_pessoa',
            'sexo': 'H' if sex == 'M' else 'M' if sex == 'F' else 'I',  # H, M and I flags are used in 4devs for filter.
            'pontuacao': 'S' if formatting else 'N',
            'idade': age,
            'cep_estado': uf_code,
            'txt_qtde': n,

            # If the state is not selected, a default flag is used for the city ('Selecione o estado!') or
            # If the state is selected and city is not selected, a default flag is used for the city ('').
            'cep_cidade': 'Selecione o estado!' if uf_code == '' else ''
        }
    )

    if data_only and r['msg'] == 'success':
        return json_loads(r['data'])
    
    if r['msg'] == 'success':

        # Convert data in str to dict.
        r['data'] = json_loads(r['data'])

        return r
    
    # In case of failure, return msg status and msg error.
    return r


def company(uf_code: str='SP', age: int=1, formatting: bool=True, data_only: bool=True) -> dict:
    """Generate random company information.
    
    Parameter
    ---------
    age
        The time of existence of the company (age of the company).
    """

    uf_code = uf_code.upper()

    raise_for_invalid_uf(uf=uf_code)

    if not (1 <= age <= 30):
        msg_error = f'The company age value "{age}" is invalid. Enter a valid company age.'
        msg_error += f' The range is 1 to 30.'

        raise ValueError(msg_error)

    r = fordev_request(
        content_length=48,
        referer='gerador_de_empresas',
        payload={
            'acao': 'gerar_empresa',
            'pontuacao': 'S' if formatting else 'N',
            'estado': uf_code,
            'idade': age
        }
    )
    
    # Replace data in html format with company info only.
    r['data'] = filter_company_info(r['data'])

    return data_format(data_only=data_only, data_dict=r)


def uf(n: int=1, data_only: bool=True) -> list:
    """Random generation of UF(Unidade Federativa) code.

    Parameters
    ----------
    n
        A number of UF for generate random code. The range is of 1 to 27.
    """

    if not (1 <= n <= 27):
        msg_error = f'The n value "{n}" is invalid. Enter a valid number of UF.'
        msg_error += f' The range is 1 to 27 UF code.'

        raise ValueError(msg_error)
    
    full_data = {
        'msg': 'success', 
        'data': random_sample(ALL_UF_CODE, n)
        }

    if data_only:
        return full_data['data']
    else:
        return full_data


def city(uf_code: str='SP', data_only: bool=True) -> list:
    """Random city generation using state UF code."""

    uf_code = uf_code.upper()

    raise_for_invalid_uf(uf=uf_code)

    r = fordev_request(
        content_length=35,
        referer='gerador_de_pessoas',
        payload={
            'acao': 'carregar_cidades',
            'cep_estado': uf_code
        }
    )
    
    # Replace data in html format with city names only
    r['data'] = filter_city_name(r['data'])

    return data_format(data_only=data_only, data_dict=r)
