from mcp.server.mcpserver import MCPServer

from app.database import SessionLocal
from app.schemas.me import MeResponse
from app.services.me_service import get_public_portfolio


mcp = MCPServer(
    "Sagar Khatri Portfolio",
)


@mcp.tool()
def get_portfolio() -> dict:
    """
    Get Sagar Khatri's complete public portfolio information.
    """

    db = SessionLocal()

    try:
        portfolio = get_public_portfolio(db)

        response = MeResponse.model_validate(portfolio)

        return response.model_dump(mode="json")

    finally:
        db.close()


if __name__ == "__main__":
    mcp.run()