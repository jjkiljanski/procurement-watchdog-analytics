Specific column-level value constraints are defined separately at the
column level and described in the column-level documentation.

## 1.1
- `col_name`: `section_1_1`
- `section_header`: `Nazwa zamawiającego`
- `data_model`: `core`
- `example_values`:
  - `BIAŁOGARDZKIE TOWARZYSTWO BUDOWNICTWA SPOŁECZNEGO SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ`
  - `GMINA MILEJCZYCE`
  - `Samodzielny Publiczny Wojewódzki Szpital Specjalistyczny w Chełmie`
- `staging_columns`:
  - `nun_buyer_name`

## 1.2
- `col_name`: `section_1_2`
- `section_header`: `Oddział zamawiającego`
- `data_model`: `core`
- `example_values`:
  - `ZZDW Koszalin`
  - `Starostwo Powiatowe w Świdnicy`
  - `MZK Witnica`
- `staging_columns`:
  - `nun_buyer_department`

## 1.3
- `col_name`: `section_1_3`
- `section_header`: `Krajowy Numer Identyfikacyjny`
- `data_model`: `core`
- `example_values`:
  - `REGON 330920050`
  - `REGON 050658976`
  - `REGON 110196908`
- `derived_cols`:
  - `section_1_3`:
    - `fn`: `parse_national_id_value`
  - `section_1_3_type`:
    - `fn`: `parse_national_id_type`
- `staging_columns`:
  - `nun_buyer_national_id`
  - `nun_buyer_national_id_type`

## 1.4.1
- `col_name`: `section_1_4_1`
- `section_header`: `Ulica`
- `data_model`: `core`
- `example_values`:
  - `STEFANA KARDYNAŁA WYSZYŃSKIEGO 18`
  - `ul. Szkolna 5`
  - `Ceramiczna 1`
- `staging_columns`:
  - `nun_buyer_street`

## 1.4.2
- `col_name`: `section_1_4_2`
- `section_header`: `Miejscowość`
- `data_model`: `core`
- `example_values`:
  - `Białogard`
  - `Milejczyce`
  - `Chełm`
- `staging_columns`:
  - `nun_buyer_city`

## 1.4.3
- `col_name`: `section_1_4_3`
- `section_header`: `Kod pocztowy`
- `data_model`: `core`
- `example_values`:
  - `78-200`
  - `17-332`
  - `22-100`
- `staging_columns`:
  - `nun_buyer_postal_code`

## 1.4.4
- `col_name`: `section_1_4_4`
- `section_header`: `Województwo`
- `data_model`: `core`
- `example_values`:
  - `zachodniopomorskie`
  - `podlaskie`
  - `lubelskie`
- `staging_columns`:
  - `nun_buyer_province`

## 1.4.5
- `col_name`: `section_1_4_5`
- `section_header`: `Kraj`
- `data_model`: `core`
- `example_values`:
  - `Polska`
  - `Zjedn.Emiraty Arabskie`
  - `Republika Czeska`
- `staging_columns`:
  - `nun_buyer_country`

## 1.4.6
- `col_name`: `section_1_4_6`
- `section_header`: `Lokalizacja NUTS 3`
- `data_model`: `core`
- `example_values`:
  - `PL426 - Koszaliński`
  - `PL842 - Łomżyński`
  - `PL812 - Chełmsko-zamojski`
- `derived_cols`:
  - `section_1_4_6_code`:
    - `fn`: `parse_nuts3_code`
  - `section_1_4_6_name`:
    - `fn`: `parse_nuts3_name`
- `staging_columns`:
  - `nun_buyer_nuts3_code`
  - `nun_buyer_nuts3_name`

## 1.4.7
- `col_name`: `section_1_4_7`
- `section_header`: `Numer telefonu`
- `data_model`: `core`
- `example_values`:
  - `+48 94 357 99 50`
  - `562 32 54`
  - `17 86 66 060`
- `staging_columns`:
  - `nun_buyer_phone`

## 1.4.8
- `col_name`: `section_1_4_8`
- `section_header`: `Numer faksu`
- `data_model`: `core`
- `example_values`:
  - `562 32 47`
  - `BRAK`
  - `+48 95 7515021`
- `staging_columns`:
  - `nun_buyer_fax`

## 1.4.9
- `col_name`: `section_1_4_9`
- `section_header`: `Adres poczty elektronicznej`
- `data_model`: `core`
- `example_values`:
  - `biuro@tbs-bialogard.pl`
  - `gmina@milejczyce.pl`
  - `przetarg@szpitalchelm.pl`
- `staging_columns`:
  - `nun_buyer_email`

## 1.4.10
- `col_name`: `section_1_4_10`
- `section_header`: `Adres strony internetowej zamawiającego`
- `data_model`: `core`
- `example_values`:
  - `https://www.tbs-bialogard.pl/`
  - `http://bip.ug.milejczyce.wrotapodlasia.pl/`
  - `www.szpitalchelm.pl`
- `staging_columns`:
  - `nun_buyer_website`

## 1.5
- `col_name`: `section_1_5`
- `section_header`: `Rodzaj zamawiającego`
- `data_model`: `core`
- `example_values`:
  - `Zamawiający publiczny - inny zamawiający`
  - `Zamawiający publiczny - jednostka sektora finansów publicznych - jednostka samorządu terytorialnego`
  - `Zamawiający publiczny - jednostka sektora finansów publicznych - samodzielny publiczny zakład opieki zdrowotnej`
- `staging_columns`:
  - `nun_buyer_type`

## 1.6
- `col_name`: `section_1_6`
- `section_header`: `Przedmiot działalności zamawiającego`
- `data_model`: `core`
- `example_values`:
  - `Inna działalność`
  - `Ogólne usługi publiczne`
  - `Zdrowie`
- `staging_columns`:
  - `nun_buyer_main_activity`

## 2.1
- `col_name`: `section_2_1`
- `section_header`: `Numer ogłoszenia`
- `data_model`: `core`
- `example_values`:
  - `2025/BZP 00000019`
  - `2025/BZP 00000044`
  - `2025/BZP 00000064`
- `staging_columns`:
  - `nun_notice_number`

## 2.2
- `col_name`: `section_2_2`
- `section_header`: `Data ogłoszenia`
- `data_model`: `core`
- `example_values`:
  - `2025-01-01`
  - `2025-01-02`
  - `2025-01-03`
- `parser`:
  - `fn`: `parse_date_from_text`
- `staging_columns`:
  - `nun_notice_date`

## 3.1
- `col_name`: `section_3_1`
- `section_header`: `Nazwa zmienianego ogłoszenia`
- `data_model`: `core`
- `example_values`:
  - `Ogłoszenie o zamówieniu`
  - `Ogłoszenie o zmianie umowy`
  - `Ogłoszenie o wykonaniu umowy`
- `staging_columns`:
  - `nun_updated_notice_name`

## 3.2
- `col_name`: `section_3_2`
- `section_header`: `Numer zmienianego ogłoszenia w BZP`
- `data_model`: `core`
- `example_values`:
  - `2024/BZP 00665454`
  - `2024/BZP 00449953`
  - `2024/BZP 00663208`
- `staging_columns`:
  - `nun_updated_notice_number`

## 3.3
- `col_name`: `section_3_3`
- `section_header`: `Identyfikator ostatniej wersji zmienianego ogłoszenia`
- `data_model`: `core`
- `example_values`:
  - `01`
- `staging_columns`:
  - `nun_updated_notice_version`

## 3.4
- `col_name`: `section_3_4`
- `section_header`: `Identyfikator sekcji zmienianego ogłoszenia`
- `data_model`: `part.core`
- `example_values`:
  - `SEKCJA V - KWALIFIKACJA WYKONAWCÓW`
  - `SEKCJA VIII - PROCEDURA`
  - `SEKCJA III - PODSTAWOWE INFORMACJE O POSTĘPOWANIU W WYNIKU KTÓREGO ZOSTAŁA ZAWARTA UMOWA`
- `staging_columns`:
  - `nun_updated_notice_section_identifier`

## 3.4.1
- `col_name`: `section_3_4_1`
- `section_header`: `Opis zmiany, w tym tekst, który należy dodać lub zmienić`
- `data_model`: `part.part`
- `example_values`:
  - `5.4.  Nazwa i opis warunków udziału w postępowaniu`
  - `8.1.  Termin składania ofert`
  - `8.3.  Termin otwarcia ofert`
- `staging_columns`:
  - `nun_updated_notice_change_description`
