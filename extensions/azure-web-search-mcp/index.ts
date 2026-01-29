import { Client } from "@modelcontextprotocol/sdk/client";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp";

type ToolResult = {
  content: Array<
    | { type: "text"; text: string }
    | { type: "image"; data: string; mimeType: string }
    | { type: "audio"; data: string; mimeType: string }
    | { type: "resource"; resource: unknown }
    | { type: "resource_link"; uri: string; name: string }
  >;
  isError?: boolean;
  structuredContent?: Record<string, unknown>;
};

const PLUGIN_ID = "azure-web-search-mcp";

type PluginConfig = {
  mcpUrl?: string;
  timeoutMs?: number;
};

let _clientPromise: Promise<Client> | null = null;
let _clientUrl: string | null = null;
let _transport: StreamableHTTPClientTransport | null = null;

function getPluginConfig(api: any): PluginConfig {
  const cfg = api?.config?.plugins?.entries?.[PLUGIN_ID]?.config ?? {};
  return cfg as PluginConfig;
}

function getMcpUrl(api: any): string {
  const cfg = getPluginConfig(api);
  return (
    cfg.mcpUrl ||
    process.env.AZURE_WEB_SEARCH_MCP_URL ||
    "http://127.0.0.1:8000/mcp"
  );
}

async function getClient(api: any): Promise<Client> {
  const url = getMcpUrl(api);
  if (_clientPromise && _clientUrl === url) return _clientPromise;

  _clientUrl = url;
  _clientPromise = (async () => {
    const transport = new StreamableHTTPClientTransport(new URL(url));
    _transport = transport;
    const client = new Client({
      name: "azure-web-search-mcp-bridge",
      version: "0.1.0"
    });
    await client.connect(transport);
    return client;
  })();

  return _clientPromise;
}

function extractText(result: unknown): string {
  const r = result as Partial<ToolResult> & { toolResult?: unknown };

  if (typeof (r as any)?.toolResult === "string") return (r as any).toolResult;
  if ((r as any)?.toolResult != null) return JSON.stringify((r as any).toolResult);

  const blocks = Array.isArray(r.content) ? r.content : [];
  const texts = blocks
    .filter((b: any) => b && b.type === "text" && typeof b.text === "string")
    .map((b: any) => b.text);

  if (texts.length) return texts.join("\n");
  return JSON.stringify(result ?? null);
}

export default function register(api: any) {
  api.registerTool(
    {
      name: "azure_web_search",
      description:
        "Call your Azure Web Search MCP server over Streamable HTTP. Returns the server JSON string.",
      parameters: {
        type: "object",
        additionalProperties: false,
        properties: {
          query: { type: "string", description: "Search query (required)." },
          mode: {
            type: "string",
            description: "quick|agentic (default: quick).",
            enum: ["quick", "agentic"]
          },
          country: {
            type: "string",
            description: "Optional ISO 3166-1 alpha-2 country code (e.g. US, CN)."
          }
        },
        required: ["query"]
      },
      async execute(_id: string, params: any) {
        const cfg = getPluginConfig(api);
        const timeoutMs = typeof cfg.timeoutMs === "number" ? cfg.timeoutMs : 0;
        const mode = (params?.mode || "quick") as string;

        const client = await getClient(api);

        const call = client.callTool(
          {
            name: "azure_web_search",
            arguments: {
              query: params?.query,
              mode,
              country: params?.country
            }
          },
          undefined,
          timeoutMs ? { timeoutMs } : undefined
        );

        let result: unknown;
        try {
          result = await call;
        } catch (err) {
          // Reset client on transport errors so the next call reconnects.
          _clientPromise = null;
          _clientUrl = null;
          try {
            await _transport?.close();
          } catch {
            // ignore
          }
          _transport = null;
          throw err;
        }

        return {
          content: [{ type: "text", text: extractText(result) }]
        };
      }
    },
    { optional: true }
  );
}

