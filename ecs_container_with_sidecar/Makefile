clean:
	rm -f app/consumer/lambda_function.zip

bundle: clean
	cd app/consumer && zip -r lambda_function.zip .

create_image:
	cd app && ./build_and_push_image.sh

plan:
	cd infra && terraform plan

deploy:
	cd infra && terraform apply

destroy:
	cd infra && terraform destroy