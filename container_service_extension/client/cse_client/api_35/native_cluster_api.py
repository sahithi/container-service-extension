# container-service-extension
# Copyright (c) 2020 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

from dataclasses import asdict
from typing import Dict, List

import pyvcloud.vcd.client as vcd_client

from container_service_extension.client.cse_client.cse_client import CseClient
import container_service_extension.client.response_processor as response_processor  # noqa: E501
import container_service_extension.common.constants.shared_constants as shared_constants  # noqa: E501
import container_service_extension.rde.models as def_models


class NativeClusterApi(CseClient):
    def __init__(self, client: vcd_client.Client):
        super().__init__(client)
        self._uri = f"{self._uri}/{shared_constants.CSE_URL_FRAGMENT}/{ shared_constants.CSE_3_0_URL_FRAGMENT}"  # noqa: E501
        self._clusters_uri = f"{self._uri}/clusters"
        self._cluster_uri = f"{self._uri}/{shared_constants.CLUSTER_URL_FRAGMENT}"  # noqa: E501

    def create_cluster(self, cluster_entity_definition: def_models.NativeEntity):  # noqa: E501
        cluster_entity_dict = asdict(cluster_entity_definition)
        uri = self._clusters_uri
        response = self._client._do_request_prim(
            shared_constants.RequestMethod.POST,
            uri,
            self._client._session,
            contents=cluster_entity_dict,
            media_type='application/json',
            accept_type='application/json')
        return def_models.DefEntity(
            **response_processor.process_response(response))

    def update_cluster_by_cluster_id(self, cluster_id, cluster_entity_definition: def_models.NativeEntity):  # noqa: E501
        cluster_entity_dict = asdict(cluster_entity_definition)
        uri = f"{self._cluster_uri}/{cluster_id}"
        response = self._client._do_request_prim(
            shared_constants.RequestMethod.PUT,
            uri,
            self._client._session,
            contents=cluster_entity_dict,
            media_type='application/json',
            accept_type='application/json')
        return def_models.DefEntity(
            **response_processor.process_response(response))

    def delete_cluster_by_cluster_id(self, cluster_id):
        uri = f"{self._cluster_uri}/{cluster_id}"
        response = self._client._do_request_prim(
            shared_constants.RequestMethod.DELETE,
            uri,
            self._client._session,
            media_type='application/json',
            accept_type='application/json')
        return def_models.DefEntity(**response_processor.process_response(response))  # noqa: E501

    def delete_nfs_node_by_node_name(self, cluster_id: str, node_name: str):
        uri = f"{self._cluster_uri}/{cluster_id}/nfs/{node_name}"
        response = self._client._do_request_prim(
            shared_constants.RequestMethod.DELETE,
            uri,
            self._client._session,
            media_type='application/json',
            accept_type='application/json')
        return def_models.DefEntity(
            **response_processor.process_response(response))

    def get_cluster_config_by_cluster_id(self, cluster_id: str) -> dict:
        uri = f"{self._cluster_uri}/{cluster_id}/config"
        response = self._client._do_request_prim(
            shared_constants.RequestMethod.GET,
            uri,
            self._client._session,
            media_type='application/json',
            accept_type='application/json')
        return response_processor.process_response(response)

    def get_upgrade_plan_by_cluster_id(self, cluster_id: str):
        uri = f'{self._cluster_uri}/{cluster_id}/upgrade-plan'
        response = self._client._do_request_prim(
            shared_constants.RequestMethod.GET,
            uri,
            self._client._session,
            accept_type='application/json')
        return response_processor.process_response(response)

    def upgrade_cluster_by_cluster_id(self, cluster_id: str,
                                      cluster_upgrade_definition: def_models.DefEntity):  # noqa: E501
        uri = f'{self._uri}/cluster/{cluster_id}/action/upgrade'
        entity_dict = asdict(cluster_upgrade_definition.entity)
        response = self._client._do_request_prim(
            shared_constants.RequestMethod.POST,
            uri,
            self._client._session,
            contents=entity_dict,
            media_type='application/json',
            accept_type='application/json')
        return def_models.DefEntity(
            **response_processor.process_response(response))

    def get_single_page_cluster_acl(self, cluster_id,
                                    page=shared_constants.CSE_PAGINATION_FIRST_PAGE_NUMBER,  # noqa: E501
                                    page_size=shared_constants.CSE_PAGINATION_DEFAULT_PAGE_SIZE):  # noqa: E501
        query_uri = f'{self._cluster_uri}/{cluster_id}/acl?' \
                    f'{shared_constants.PaginationKey.PAGE_NUMBER}={page}&' \
                    f'{shared_constants.PaginationKey.PAGE_SIZE}={page_size}'
        response = self._client._do_request_prim(
            shared_constants.RequestMethod.GET,
            query_uri,
            self._client._session,
            accept_type='application/json')
        processed_response = response_processor.process_response(response)
        return processed_response

    def list_native_cluster_acl_entries(self, cluster_id):
        page_num = 0
        while True:
            page_num += 1
            acl_response = self.get_single_page_cluster_acl(
                cluster_id=cluster_id,
                page=page_num,
                page_size=shared_constants.CSE_PAGINATION_DEFAULT_PAGE_SIZE)
            acl_values = acl_response['values']
            if len(acl_values) == 0:
                break
            for acl_value in acl_values:
                yield def_models.ClusterAclEntry(**acl_value)

    def put_cluster_acl(self, cluster_id: str, acl_entries: List[Dict]):
        uri = f'{self._cluster_uri}/{cluster_id}/acl'
        put_content = {shared_constants.ClusterAclKey.ACCESS_SETTING:
                       acl_entries}
        response = self._client._do_request_prim(
            shared_constants.RequestMethod.PUT,
            uri,
            self._client._session,
            contents=put_content,
            media_type='application/json',
            accept_type='application/json')
        response_processor.process_response(response)
