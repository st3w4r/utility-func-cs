from pygls.client import JsonRPCClient
from pygls.protocol import LanguageServerProtocol
import asyncio
from lsprotocol.types import (
    ClientCapabilities,
    TextDocumentClientCapabilities,
    TextDocumentSyncClientCapabilities,
    CompletionClientCapabilities,
    CompletionClientCapabilitiesCompletionItemType,
    WorkspaceClientCapabilities,
    WorkspaceEditClientCapabilities,
    InitializeParams,
    DidOpenTextDocumentParams,
    TextDocumentItem,
    DocumentSymbolParams,
    Position,
    Range,
    TextDocumentIdentifier
)
from pygls.exceptions import JsonRpcException

class CustomLspClient(JsonRPCClient):
    def __init__(self):
        self.name = 'CustomLspClient'
        self.version = '0.1.0'
        self.protocol = LanguageServerProtocol(self, asyncio.get_event_loop())
        super().__init__(protocol_cls=LanguageServerProtocol)

    async def connect(self, host, port):
        reader, writer = await asyncio.open_connection(host, port)
        await self.start(reader, writer)

    async def initialize(self, root_uri):
        client_capabilities = ClientCapabilities(
            text_document=TextDocumentClientCapabilities(
                synchronization=TextDocumentSyncClientCapabilities(
                    dynamic_registration=True,
                    will_save=True,
                    will_save_wait_until=True,
                    did_save=True
                ),
                completion=CompletionClientCapabilities(
                    dynamic_registration=True,
                    completion_item=CompletionClientCapabilitiesCompletionItemType(
                        snippet_support=True
                    )
                )
            ),
            workspace=WorkspaceClientCapabilities(
                apply_edit=True,
                workspace_edit=WorkspaceEditClientCapabilities(
                    document_changes=True
                )
            )
        )
        params = InitializeParams(
            process_id=None,
            root_uri=root_uri,
            capabilities=client_capabilities
        )
        return self.protocol.send_request('initialize', params)

    async def start(self, reader, writer):
        self.loop = asyncio.get_event_loop()
        self.protocol.connection_made(writer)
        asyncio.ensure_future(self._data_received(reader))

    async def _data_received(self, reader):
        while True:
            data = await reader.read(4096)
            if not data:
                break
            self.protocol.data_received(data)
    
    async def send_notification(self, method, params):
        self.protocol.notify(method, params)


    async def get_imports(self, uri):
        params = DocumentSymbolParams(
            text_document=TextDocumentIdentifier(uri=uri)
        )
        response = self.protocol.send_request('textDocument/documentSymbol', params)

        response.result()

        if response:
            import_statements = [symbol for symbol in response if symbol.kind == 3]  # Assuming kind 3 corresponds to imports
            return import_statements
        return []

async def main():
    host = 'localhost'
    port = 2087

    client = CustomLspClient()
    await client.connect(host, port)

    # Send initialize request
    try:
        response = await client.initialize('file:///workspaces/interview/codestory')
        print(response.result())
    except JsonRpcException as e:
        print(f"Error init: {e}")

        text_document_item = TextDocumentItem(
            uri='file:///workspaces/interview/codestory/src/llm.py',
            language_id='python',
            version=1,
            text='print("Hello, World!")'
        )

        did_open_params = DidOpenTextDocumentParams(
            text_document=text_document_item
        )
        res = await client.send_notification('textDocument/didOpen', did_open_params)

        print(res)
        print("Notification sent")

    # Send a custom notification
    try:
        text_document_item = TextDocumentItem(
            uri='file:///workspaces/interview/codestory/test.py',
            language_id='python',
            version=1,
            text='print("Hello, World!")'
        )
        did_open_params = DidOpenTextDocumentParams(
            text_document=text_document_item
        )
        client.send_notification('textDocument/didOpen', did_open_params)
        print("Notification sent")
    except JsonRpcException as e:
        print(f"Error sending notification: {e}")

    # Retrieve and print import statements
    try:
        imports = await client.get_imports('file:///workspaces/interview/codestory/src/llm.py')
        for imp in imports:
            print(imp.name)
    except JsonRpcException as e:
        print(f"Error retrieving imports: {e}")

if __name__ == "__main__":
    asyncio.run(main())
