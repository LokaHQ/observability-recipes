clean:
	rm -f app/consumer/lambda_function.zip
	rm -f app/producer/lambda_function.zip

bundle: clean
	cd app/consumer && zip -r lambda_function.zip .
	cd app/producer && zip -r lambda_function.zip .


plan:
	cd infra && terraform plan

deploy:
	cd infra && terraform apply

destroy:
	cd infra && terraform destroy