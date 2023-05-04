from api.models.index import db, Company, Services
import api.domain.services.repository as Repository

def create_new_service(company_id, current_user_id, body):
    company = Company.query.get(company_id)
    if company is None:
        return {'msg': f'The Company with id: {company_id}, do not exists in this database.', 'status': 404}

    if current_user_id != company.user_id:
        return {'msg': 'You do not have rights to create new services!', 'status': 403}

    return Repository.create_new_service(body, company_id)

def get_services_by_company(company_id):
    company = Company.query.get(company_id)
    if company is None:
        return {'msg': f'The Company with id: {company_id}, do not exists in this database.', 'status': 404}

    services = Repository.get_services_by_company(company_id)
    return services

def get_single_service(service_id):
    service = Repository.get_single_service(service_id)
    if service is None:
        return {'msg': f'Service with id: {service_id}, do not exists in this database.', 'status': 404}

    return service

def delete_service(service_id, current_user_id):
    service = Services.query.get(service_id)
    if service is None:
        return {'msg': f'Service with id: {service_id}, do not exists in this database.', 'status': 404}
        
    service_company_id = service.company_id
    user_id = Company.query.get(service_company_id).user_id

    if current_user_id != user_id:
        return {'msg': 'You do not have rights to delete services!', 'status': 403}

    deleted_service = Repository.delete_service(service_id)
    return deleted_service
