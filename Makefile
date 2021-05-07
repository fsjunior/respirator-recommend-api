.PHONY: generate-migrations
include .env
export

clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.log" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f .coverage.NB-SBDEV*

require:
	@echo "Checking the programs required for the build are installed..."
	@command -v poetry >/dev/null 2>&1 || (echo "ERROR: Poetry is required. Aborting..."; exit 1)
	@command -v docker-compose >/dev/null 2>&1 || (echo "ERROR: docker-compose is required. Aborting..."; exit 1)
	@echo "All dependencies meet"

build-env: require
	poetry install
	poetry run pre-commit install


test: clean
	poetry run pytest test
	poetry run pytest --dead-fixtures --dup-fixtures test

check-all: coverage
	pre-commit run --all-files

coverage: clean
	poetry run pytest --dead-fixtures --dup-fixtures test
	poetry run pytest test --cov --cov-fail-under=85 --cov-report=term-missing

coverage-update: coverage
	poetry run codecov

run-dev:
	poetry run python run.py

generate-validation-data:
	mkdir -p test/data
	poetry run python utils/generate_validation_data.py \
		"https://www.superepi.com.br/mascara-bls-pff2-sem-valvula-bls-tipo-concha-128-b-1835-p1052423" \
		--dest-dir validation/data/ --respirator_type PFF2 --no-exhalation-valve --quantity 1 --price 6.59 \
		--approval-certificate 33803
	poetry run python utils/generate_validation_data.py \
		"https://www.lojadomecanico.com.br/produto/164416/36/314/mascara-respiratoria-semifacial-n95-pff2-s-tipo-concha-com-20-unidades-3m-hb004116743-" \
		--dest-dir validation/data/ --respirator_type PFF2 --quantity 20 --price 349.90
	poetry run python utils/generate_validation_data.py \
		"https://www.claruscomercial.com.br/epi/respiradores/respirador-desc-gvs-pff2-sv-ca-38337" \
		--dest-dir validation/data/ --respirator_type PFF2 --no-exhalation-valve --quantity 1 --price 4.75 \
		--approval-certificate 38337
	poetry run python utils/generate_validation_data.py "https://www.lupo.com.br/mascara-bacoff-36004-900/p" \
		--dest-dir validation/data/ --spandex --quantity 2 --price 21.90
	poetry run python utils/generate_validation_data.py "https://www.insiderstore.com.br/produto/mascara-antiviral-355" \
		--dest-dir validation/data/ --spandex --quantity 1 --price 25.0
	poetry run python utils/generate_validation_data.py \
		"https://produto.mercadolivre.com.br/MLB-1570176367-mascara-respiratoria-pff2-tipo-n95-s-valvula-10-unidades-_JM#position=5&type=item&tracking_id=02afacc7-31e6-47f0-9b2c-cfe5438f6da2" \
		--dest-dir validation/data/ --respirator_type PFF2 --no-exhalation-valve --quantity 10 --price 48.90
	poetry run python utils/generate_validation_data.py \
		"https://produto.mercadolivre.com.br/MLB-1792013183-kit-10-mascaras-n95-proteco-respiratoria-pff2-full-_JM#searchVariation=75894871640&position=2&type=pad&tracking_id=02afacc7-31e6-47f0-9b2c-cfe5438f6da2&is_advertising=true&ad_domain=VQCATCORE_LST&ad_position=2&ad_click_id=NDJjMmU3YWYtZDcwMy00YmJjLThlZTAtMDVhMTcxNjI1NDY0" \
		--dest-dir validation/data/ --respirator_type PFF2 --quantity 10 --price 29.99
	poetry run python utils/generate_validation_data.py \
		"https://produto.mercadolivre.com.br/MLB-1537516387-10-mascaras-respiratoria-pff2-tipo-n95-s-valvula-delta-plus-_JM?searchVariation=56833158472#searchVariation=56833158472&position=2&type=item&tracking_id=1052afce-4810-4b9f-a83a-bfb95a31b482" \
		--dest-dir validation/data/ --respirator_type PFF2 --no-exhalation-valve --quantity 10 --price 29.99
	poetry run python utils/generate_validation_data.py \
		"https://www.amazon.com.br/M%C3%A1scara-Respirat%C3%B3ria-V%C3%A1lvula-Delta-Plus/dp/B08Z8CWK1P/ref=zg_bs_17114284011_2?_encoding=UTF8&psc=1&refRID=RTX5XF8DZ92987ZSP2RK" \
		--dest-dir validation/data/ --respirator_type PFF2 --no-exhalation-valve --quantity 10 \
		--approval-certificate 38504 --price 39.90

validate:
	poetry run pytest validation

generate-migrations:
	pymongo-migrate generate -u $(MONGO_URL) -m migrations
	echo "Migration template generated in 'migrations' directory. Please review the generated file."

apply-migrations:
	pymongo-migrate migrate -u $(MONGO_URL) -m migrations

