describe("template spec", () => {
  it("shows history", () => {
    cy.visit("http://localhost:8501");
    cy.get('a[href="http://localhost:8501/History"]').click();
    cy.get('input[aria-label*="Email"]').type("ucet.pc212@gmail.com");
    cy.get('input[aria-label*="Password"]').type("573y16f5");
    cy.get('button[data-testid="baseButton-secondary"]').click();
    cy.contains("td", "whooo").should("be.visible");
  });
  it("shows jobs", () => {
    cy.visit("http://localhost:8501");
    cy.contains("label", "Median Pay").should("be.visible");
    cy.contains("label", "Number of jobs").should("be.visible");
    cy.get("canvas").should("exist");
    cy.get('div[class="dvn-scroller glideDataEditor"]').should("exist");
    cy.get("iframe").should("exist");
  });
  it("can ask video", () => {
    cy.visit("http://localhost:8501");
    cy.get('a[href="http://localhost:8501/Ask_a_video"]').click();
    cy.get('input[aria-label*="Email"]').type("ucet.pc212@gmail.com");
    cy.get('input[aria-label*="Password"]').type("573y16f5");
    cy.get('button[data-testid="baseButton-secondary"]').click();
    cy.get('input[aria-label*="YouTube"]').type(
      "https://www.youtube.com/watch?v=q7KqVQ77BNY"
    );
    cy.get('input[aria-label*="Ask a question"]').type(
      "What does the speaker say about Atomic Habits?"
    );
    cy.get('button[data-testid="baseButton-secondary"]').click();
    cy.wait(5000);
    cy.get('iframe[title="streamlit_player.streamlit_player"]').should(
      "be.visible",
      { timeout: 10000 }
    );
    cy.wait(120000);
    cy.contains("div", "Atomic Habits").should("be.visible");
  });
});
